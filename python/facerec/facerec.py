# a mashup of facerec_from_webcam_faster.py
# from https://github.com/ageitgey/face_recognition
# and `face-postgre` from https://github.com/vearutop/face-postgre

import os
import cv2
import sys
import yaml
import dlib
import numpy
import postgresql
import face_recognition
from datetime import datetime

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other
# demos that don't require it instead.

if len(sys.argv) < 3:
    print("USAGE : facerec <deviceid|mjpegurl|file> <configfile>")
    print("SAMPLE: facerec 0 ./conf.sample.yml")
    print("        facerec http://example.com/axis-cgi/mjpg/video.cgi?camera=3 ./conf.sample.yml")
    exit(1)

if not os.path.exists("./.faces"):
    os.mkdir("./.faces")


class FacerecPG:

    def __init__(self, config: str):
        self.conf = yaml.safe_load(open(config))
        self.db = postgresql.open('pq://{}:{}@{}:{}/{}'.format(
            self.conf['postgres']['user'],
            self.conf['postgres']['pass'],
            self.conf['postgres']['host'],
            self.conf['postgres']['port'],
            self.conf['postgres']['db']))

    def findfaces(self, enc: numpy.ndarray, limit: int) -> list:
        query = "SELECT file, split_part(p.name,' ',1) as name \
                FROM vectors  v \
                LEFT OUTER JOIN profiles p ON v.profile_id = p.id \
                ORDER BY " + \
                "(CUBE(array[{}]) <-> vec_low) + (CUBE(array[{}]) <-> vec_high) \
                ASC LIMIT {}".format(
                    ','.join(str(s) for s in enc[0:63]),
                    ','.join(str(s) for s in enc[64:127]),
                    limit,
                )
        return self.db.query(query)


class FacerecVideo:

    def __init__(self, source: str):
        if source.isdigit():
            self.capture, self.info = cv2.VideoCapture(
                int(0)), "<device {}>".format(source)
        else:
            self.capture, self.info = cv2.VideoCapture(
                source), "<{}>".format(source)


frvideo = FacerecVideo(sys.argv[1])
print("- using video at " + frvideo.info)

fr = FacerecPG(sys.argv[2])
print("- using DB at {}:{}/{}".format(fr.conf['postgres'][
      'host'], fr.conf['postgres']['port'], fr.conf['postgres']['db']))

print("- configuring environment..")
FONT = cv2.FONT_HERSHEY_DUPLEX
FONT_SCALE = 0.5
FONT_THICKNESS = 1

RGB_WHITE = (255, 255, 255)
RGB_LIME = (0, 255, 0)
RGB_RED = (0, 0, 255)
RECT_COLOR = RGB_RED  # red

# feedback duration in frames
DEFAULT_FEEDBACK_DURATION = 7

DEFAULT_FACE_LABEL = "Unknown"

WINDOW_NAME = 'Video source: {}'.format(frvideo.info)
UP_SINCE = "[FACEREC] UP SINCE {}".format(
    datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
KEY_HINTS = "q: quit, r: record, s: screenshot, v or h: flip"

# Create a HOG face detector using the built-in dlib class
face_detector = dlib.get_frontal_face_detector()

storage = {
    "screenshots": '{}/screenshots'.format(fr.conf["storage"]),
    "recordings": '{}/recordings'.format(fr.conf["storage"]),
}
for key, path in storage.items():
    if not os.path.exists(path):
        print("- creating '{}' storage at {}".format(key, path))
        os.makedirs(path)

# using constants from opencv3 (depends on what's installed)
frameHeight = frvideo.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
frameWidth = frvideo.capture.get(cv2.CAP_PROP_FRAME_WIDTH)

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
runtimeFlipH = False
runtimeFlipV = False
feedbacks = {
    'demoalert': {
        'duration': 0,
        'text': "Demo mode is enabled: press ctrl+c in console to quit",
        'color': RGB_RED,
        'flashcolor': None,
    },
    'screenshots': {
        'duration': 0,
        'text': "Screenshot saved!",
        'color': RGB_LIME,
        'flashcolor': RGB_LIME,
    },
    'recordingstarted': {
        'duration': 0,
        'text': "Recording started",
        'color': RGB_LIME,
        'flashcolor': None,
    },
    'recordingstopped': {
        'duration': 0,
        'text': "Recording stopped",
        'color': RGB_RED,
        'flashcolor': None,
    },
}


class Recorder:

    def __init__(self, framesize: (int, int), storagepath: str, start: bool):
        self.writer = None
        self.isrecording = start
        self.storagepath = storagepath
        self.frameheight = framesize[0]
        self.framewidth = framesize[1]

        if self.isrecording:
            self.record()

    def close(self) -> bool:
        if self.writer is None:
            return None

        self.writer.release()
        return True

    def record(self):
        now = datetime.now()
        self.writer = cv2.VideoWriter(
            '{}/{}.avi'.format(
                self.storagepath,
                now.strftime('%Y-%m-%d_%H%M%S')),
            cv2.VideoWriter_fourcc(*"X264"),
            20.0,
            (self.framewidth, self.frameheight))


rc = Recorder((int(frameHeight),
               int(frameWidth)),
              storage['recordings'],
              fr.conf['frame']['recordonstart'])
print("- recording status: {}".format(rc.isrecording))

if not fr.conf["window"]["enabled"]:
    print("- activating facerec without window")
else:
    print("- configuring window")
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)

print("facerec is activated")
print(UP_SINCE)

while frvideo.capture.isOpened():
    # Grab a single frame of video
    ret, frame = frvideo.capture.read()
    if not ret:
        continue

    if fr.conf["frame"]["flip"]["horizontal"] or runtimeFlipH:
        frame = cv2.flip(frame, 0)
    if fr.conf["frame"]["flip"]["vertical"] or runtimeFlipV:
        frame = cv2.flip(frame, 1)

    cv2.putText(frame,
                UP_SINCE,
                (10, int(frameHeight) - 10),
                FONT,
                FONT_SCALE - 0.1,
                (255, 255, 255),
                FONT_THICKNESS)

    ret, baseline = cv2.getTextSize(
        KEY_HINTS,
        FONT,
        FONT_SCALE - 0.1,
        FONT_THICKNESS)
    textWidth = ret[0] + 6
    keyHintsAxis = (int(frameWidth) - textWidth, int(frameHeight) - 10)
    cv2.putText(frame,
                KEY_HINTS,
                keyHintsAxis,
                FONT,
                FONT_SCALE - 0.1,
                (255, 255, 255),
                FONT_THICKNESS)

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which
    # face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(
            rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s) in db
            rows = fr.findfaces(face_encoding, 1)
            if len(rows) == 0:
                name = DEFAULT_FACE_LABEL
            else:
                file, profilename = rows[0]
                if profilename:
                    name = profilename
                else:
                    filename = os.path.basename(file)
                    name = os.path.splitext(filename)[0]
                    name = name.replace("_", " ").replace("-", " ")

            face_names.append(name)
            print("face detected: " + name)

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was
        # scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), RECT_COLOR, 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 25),
                      (right, bottom), RECT_COLOR, cv2.FILLED)
        cv2.putText(frame, name, (left + 6, bottom - 6), FONT,
                    FONT_SCALE, (255, 255, 255), FONT_THICKNESS)

    # Display feedback frames
    for i, f in feedbacks.items():
        if f['duration']:
            if f['flashcolor']:
                cv2.rectangle(frame,
                              (0, 0),
                              (int(frameWidth), int(frameHeight)),
                              f['flashcolor'],
                              4)
            scale = FONT_SCALE - 0.1
            ret, baseline = cv2.getTextSize(
                f['text'],
                FONT,
                scale,
                FONT_THICKNESS)
            textWidth = ret[0] + 6
            axis = (int(frameWidth) - textWidth, int(frameHeight) - 30)
            cv2.putText(frame,
                        f['text'],
                        axis,
                        FONT,
                        scale,
                        f['color'],
                        FONT_THICKNESS)
            f['duration'] -= 1

    if rc.writer is not None and rc.isrecording:
        x, y = keyHintsAxis
        cv2.putText(frame,
                    '[R]',
                    (x - 23, y + 1),
                    FONT,
                    FONT_SCALE - 0.1,
                    RGB_RED,
                    FONT_THICKNESS)
        rc.writer.write(frame)

    # Display the resulting image in window
    if fr.conf["window"]["enabled"]:
        cv2.imshow(WINDOW_NAME, frame)

    c = cv2.waitKey(1)
    # Hit 'q' on the keyboard to quit!
    if c == ord('q'):
        if fr.conf['window']['enabled'] and fr.conf['window']['demomode']:
            feedbacks['demoalert']['duration'] = DEFAULT_FEEDBACK_DURATION
        else:
            break

    elif c == ord('h'):
        runtimeFlipH = not runtimeFlipH

    elif c == ord('v'):
        runtimeFlipV = not runtimeFlipV

    elif c == ord('r'):
        rc.isrecording = not rc.isrecording
        if rc.isrecording:
            rc.record()
            feedbacks['recordingstarted'][
                'duration'] = DEFAULT_FEEDBACK_DURATION
        else:
            feedbacks['recordingstopped'][
                'duration'] = DEFAULT_FEEDBACK_DURATION
        print('[RECORDING] {}'.format(rc.isrecording))

    elif c == ord('s'):
        now = datetime.now()
        filename = '{}/{}_{}.jpg'.format(
            storage["screenshots"],
            now.strftime('%Y-%m-%d_%H%M%S'),
            now.microsecond)
        cv2.imwrite(filename, frame)
        feedbacks['screenshots']['duration'] = DEFAULT_FEEDBACK_DURATION
        print('[SAVED] {}'.format(filename))

print("Exit routine started..")

if rc.close() is not None:
    print("- stopping recorder")

print("- stopping video capture")
# Release handle to the webcam
frvideo.capture.release()
cv2.destroyAllWindows()

print("[EXIT] facerec exited")
