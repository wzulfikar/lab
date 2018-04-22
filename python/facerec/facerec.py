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

BGR_WHITE = (255, 255, 255)
BGR_LIME = (0, 255, 0)
BGR_RED = (0, 0, 255)
RECT_COLOR = BGR_RED  # red

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

feedbacks = {
    'demoalert': {
        'duration': 0,
        'text': "Demo mode is enabled: press ctrl+c in console to quit",
        'color': BGR_RED,
        'flashcolor': None,
    },
    'screenshots': {
        'duration': 0,
        'text': "Screenshot saved!",
        'color': BGR_LIME,
        'flashcolor': BGR_LIME,
    },
    'recordingstarted': {
        'duration': 0,
        'text': "Recording started",
        'color': BGR_LIME,
        'flashcolor': None,
    },
    'recordingstopped': {
        'duration': 0,
        'text': "Recording stopped",
        'color': BGR_RED,
        'flashcolor': None,
    },
    'unknown_face': {
        'duration': 0,
        'text': "unknown face detected",
        'color': BGR_RED,
        'flashcolor': None,
    },
    'on_enter': {
        'duration': 0,
        'text': "Hello {}!",
        'color': BGR_LIME,
        'flashcolor': None,
    },
    'on_leaving': {
        'duration': 0,
        'text': "{} has left",
        'color': BGR_RED,
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

runtime_vars = {
    'quitting': False,
    'flip_h': fr.conf["frame"]["flip"]["horizontal"],
    'flip_v': fr.conf["frame"]["flip"]["vertical"],
    'window_enabled': fr.conf['window']['enabled'],
    'demomode': fr.conf['window']['demomode'],
    'current_fps': 0,
}

# activate pipelines
p_reg = PipelineRegister([('lookback'),
                          ('display_info',
                           runtime_vars,
                           KEY_HINTS),
                          ('display_feedbacks',
                           feedbacks,
                           DEFAULT_FEEDBACK_DURATION),
                          ('draw_face_labels', fr.findfaces),
                          ('presence'),
                          ('recorder',
                           frvideo.capture,
                           storage['recordings'],
                           fr.conf['frame']['recordonstart']),
                          ('key_press',
                           runtime_vars,
                           storage['screenshots'],
                           runtime_vars['window_enabled'],
                           runtime_vars['demomode'])])
pipelines = p_reg.pipelines

rc = pipelines['recorder']
print("- recording status: {}".format(rc.isrecording))

print("facerec is activated")

while frvideo.capture.isOpened():
    # Grab a single frame of video
    ret, frame = frvideo.capture.read()
    if not ret:
        continue

    if runtime_vars['flip_h']:
        frame = cv2.flip(frame, 0)
    if runtime_vars['flip_v']:
        frame = cv2.flip(frame, 1)

    # run the pipelines
    w, h = int(framewidth), int(frameheight)
    pipelines['display_info'].process(frame, w, h, rc.isrecording)
    pipelines['display_feedbacks'].process(frame, w, h)
    pipelines['draw_face_labels'].process(frame, w, h)
    pipelines['lookback'].process(frame)
    pipelines['recorder'].process(frame)
    pipelines['presence'].process(frame)

    c = cv2.waitKey(1)
    pipelines['key_press'].process(frame, c)

    if runtime_vars['quitting']:
        break

    # Display the resulting image in window
    if runtime_vars['window_enabled']:
        cv2.imshow(WINDOW_NAME, frame)


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
