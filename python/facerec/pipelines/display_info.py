import numpy as np
import cv2


def display_info(pipeline, frame: np.ndarray, w: int, h: int,
                 args: tuple):
    fps_current, key_hints = args

    cv2.putText(frame,
                pipeline.labels['up_since'],
                (10, h - 10),
                pipeline.defaults['font'],
                pipeline.defaults['font_scale'] - 0.1,
                (255, 255, 255),
                pipeline.defaults['font_thickness'])

    if fps_current is not None:
        if fps_current > 0:
            cv2.putText(frame,
                        "{0:.1f} fps".format(fps_current),
                        (10, h - 25),
                        pipeline.defaults['font'],
                        pipeline.defaults['font_scale'] - 0.1,
                        (255, 255, 255),
                        pipeline.defaults['font_thickness'])
        else:
            cv2.putText(frame,
                        "calculating fps..".format(fps_current),
                        (10, h - 25),
                        pipeline.defaults['font'],
                        pipeline.defaults['font_scale'] - 0.1,
                        (255, 255, 255),
                        pipeline.defaults['font_thickness'])

    ret, baseline = cv2.getTextSize(
        key_hints,
        pipeline.defaults['font'],
        pipeline.defaults['font_scale'] - 0.1,
        pipeline.defaults['font_thickness'])
    textWidth = ret[0] + 6
    keyHintsAxis = (w - textWidth, h - 10)
    cv2.putText(frame,
                key_hints,
                keyHintsAxis,
                pipeline.defaults['font'],
                pipeline.defaults['font_scale'] - 0.1,
                (255, 255, 255),
                pipeline.defaults['font_thickness'])
