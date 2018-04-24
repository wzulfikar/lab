# a mashup of facerec_from_webcam_faster.py
# from https://github.com/ageitgey/face_recognition
# and `face-postgre` from https://github.com/vearutop/face-postgre
# 
# Note: install OpenCV (the `cv2` library) if you want to read from webcam

import os
import cv2
import sys
import yaml
import dlib
import numpy

from lib.video_capture import VideoCapture
import lib.frame_loop as frame_loop

# import user config for pipelines and event listeners
import event_listeners
import register_pipelines

if len(sys.argv) < 3:
    print("USAGE : iris <deviceid|mjpegurl|file> <configfile>")
    print("SAMPLE: iris 0 ./conf.sample.yml")
    print("        iris http://example.com/axis-cgi/mjpg/video.cgi?camera=3 ./conf.sample.yml")
    exit(1)

if not os.path.exists("./.faces"):
    os.mkdir("./.faces")

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


def _configure(conf: dict, frvideo, w: int, h: int):
    # using constants from opencv3 (depends on what's installed)
    device_fps = frvideo.capture.get(cv2.CAP_PROP_FPS)
    print("- video capture fps:", device_fps)

    if not conf["window"]["enabled"]:
        print("- activating facerec without window")
    else:
        print("- configuring window")
        print("- current width x height:", w, h)
        minsize, maxsize = "", ""
        if 'minsize' in conf['frame']:
            minsize = conf['frame']['minsize']
        if 'maxsize' in conf['frame']:
            maxsize = conf['frame']['maxsize']

        currentwh, err = adjust_frame_size(frvideo.capture, minsize, maxsize)
        if err is not None:
            print("Failed to adjust frame size:", err)
            exit(1)
        else:
            framewidth, frameheight = currentwh

if __name__ == '__main__':
    print("- configuring environment..")
    
    frvideo = VideoCapture(sys.argv[1])
    print("- using video at " + frvideo.info)

    WINDOW_NAME = 'Video source: {}'.format(frvideo.info)

    conf = yaml.safe_load(open(sys.argv[2]))
    runtime_vars = {
        'quitting': False,
        'flip_h': conf["frame"]["flip"]["horizontal"],
        'flip_v': conf["frame"]["flip"]["vertical"],
        'framewidth': int(frvideo.capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
        'frameheight': int(frvideo.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        'window_enabled': conf['window']['enabled'],
        'demomode': conf['window']['demomode'],
        'current_fps': 0,
        'window_name': WINDOW_NAME,
    }

    _configure(conf, frvideo, runtime_vars['framewidth'], runtime_vars['frameheight'])
    
    # activate pipelines
    hooks = event_listeners.register()
    p_reg = register_pipelines.register(hooks=hooks, 
                                        runtime_vars=runtime_vars, 
                                        conf=conf,
                                        video_capture=frvideo.capture)

    print("- recording status: {}".format(p_reg.pipelines['recorder'].isrecording))

    print("facerec is activated")
    frame_loop.loop(frvideo, runtime_vars, p_reg)
    
    print("Exit routine started..")
    p_reg.close_pipelines()

    print("- stopping video capture")
    # Release handle to the webcam
    frvideo.capture.release()
    cv2.destroyAllWindows()

    print("[EXIT] facerec exited")