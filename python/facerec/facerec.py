# a mashup of facerec_from_webcam_faster.py
# from https://github.com/ageitgey/face_recognition
# and `face-postgre` from https://github.com/vearutop/face-postgre

import os
import cv2
import sys
import yaml
import time
import dlib
import numpy
import postgresql
from datetime import datetime

# import pipelines
from pipelines.pipeline_register import PipelineRegister

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
# 2. Only detect faces in every other frame of video (calculate using
# `fps_counter`).

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
        query = "SELECT file, p.id as profile_id, p.name as name \
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


def adjust_frame_size(video_capture, minwh, maxwh) -> ((int, int), str):
    max_w, max_h, min_w, min_h = 0, 0, 0, 0

    if minwh != "":
        w, h = minwh.split(',')
        min_w, min_h = int(w), int(h)
    if maxwh != "":
        w, h = maxwh.split(',')
        max_w, max_h = int(w), int(h)

    if (maxwh != "" and minwh != "") and (min_w > max_w or min_h > max_h):
        return ((0, 0), "error: conflict in min and max size")

    currentwidth = video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    currentheight = video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

    if max_w > 0 and max_h > 0:
        if max_w < currentwidth:
            print("- adjusting max width to:", max_w)
            currentwidth = float(max_w)
            video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, max_w)

        if max_h < currentheight:
            print("- adjusting max height to:", max_h)
            currentheight = float(max_h)
            video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, max_h)

    if min_w > 0 and min_h > 0:
        if min_w > currentwidth:
            print("- adjusting min width to:", min_w)
            video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, min_w)

        if min_h > currentheight:
            print("- adjusting min height to:", min_h)
            video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, min_h)

    return (currentwidth, currentheight), None


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
frameheight = frvideo.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
framewidth = frvideo.capture.get(cv2.CAP_PROP_FRAME_WIDTH)
device_fps = frvideo.capture.get(cv2.CAP_PROP_FPS)
print("- video capture fps:", device_fps)

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

if not fr.conf["window"]["enabled"]:
    print("- activating facerec without window")
else:
    print("- configuring window")
    print("- current width x height:", framewidth, frameheight)
    minsize, maxsize = "", ""
    if 'minsize' in fr.conf['frame']:
        minsize = fr.conf['frame']['minsize']
    if 'maxsize' in fr.conf['frame']:
        maxsize = fr.conf['frame']['maxsize']

    currentwh, err = adjust_frame_size(frvideo.capture, minsize, maxsize)
    if err is not None:
        print("Failed to adjust frame size:", err)
        exit(1)
    else:
        framewidth, frameheight = currentwh

# activate pipelines
p_reg = PipelineRegister(fr.findfaces, pipelines=['display_info',
                                                  'display_feedbacks',
                                                  'draw_face_labels',
                                                  'lookback',
                                                  'presence',
                                                  'recorder'])
pipelines = p_reg.pipelines

rc = pipelines['recorder']
rc.set_args(frvideo.capture,
            storage['recordings'],
            fr.conf['frame']['recordonstart'])
print("- recording status: {}".format(rc.isrecording))

print("facerec is activated")

fps_time = time.time()
fps_counter = 0
fps_current = 0
while frvideo.capture.isOpened():
    # Grab a single frame of video
    ret, frame = frvideo.capture.read()
    if not ret:
        continue

    if fr.conf["frame"]["flip"]["horizontal"] or runtimeFlipH:
        frame = cv2.flip(frame, 0)
    if fr.conf["frame"]["flip"]["vertical"] or runtimeFlipV:
        frame = cv2.flip(frame, 1)

    # run the pipelines
    w, h = int(framewidth), int(frameheight)
    pipelines['display_info'].process(frame, w, h, (fps_current, KEY_HINTS))
    pipelines['display_feedbacks'].process(frame, w, h, (feedbacks))
    pipelines['draw_face_labels'].process(frame, w, h)
    pipelines['lookback'].process(frame)
    pipelines['recorder'].process(frame)

    # get location of key hints (drawn in `pipeline.draw_info`)
    ret, baseline = cv2.getTextSize(
        KEY_HINTS,
        FONT,
        FONT_SCALE - 0.1,
        FONT_THICKNESS)
    textWidth = ret[0] + 6
    keyHintsAxis = (int(framewidth) - textWidth, int(frameheight) - 10)

    if rc.isrecording:
        x, y = keyHintsAxis
        cv2.putText(frame,
                    '[R]',
                    (x - 23, y + 1),
                    FONT,
                    FONT_SCALE - 0.1,
                    RGB_RED,
                    FONT_THICKNESS)

    c = cv2.waitKey(1)

    # Display the resulting image in window
    if fr.conf["window"]["enabled"]:
        cv2.imshow(WINDOW_NAME, frame)
        fps_counter += 1

    # update `fps_current`
    if fps_counter == 20:
        seconds = time.time() - fps_time
        fps_time = time.time()
        fps_current = fps_counter / seconds
        fps_counter = 0
        print("- current fps:", fps_current)

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
            fps_record_adjustment = 2
            rc.start_recording(int(fps_current) + fps_record_adjustment)
            feedbacks['recordingstarted'][
                'duration'] = DEFAULT_FEEDBACK_DURATION
        else:
            rc.stop_recording()
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

print("- executing pipeline `closer` method..")
for pipeline_name, pipeline in pipelines.items():
    if hasattr(pipeline, 'closer') and callable(getattr(pipeline, 'closer')):
        pipeline.closer()
        print("pipeline closed:", pipeline_name)


print("- stopping video capture")
# Release handle to the webcam
frvideo.capture.release()
cv2.destroyAllWindows()

print("[EXIT] facerec exited")
