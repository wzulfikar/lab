import numpy as np

import cv2


def display_feedbacks(pipeline, frame: np.ndarray, w: int, h: int,
                      args: tuple):
    feedbacks = args
    # display feedback frames
    for i, f in feedbacks.items():
        if f['duration']:
            if f['flashcolor']:
                cv2.rectangle(frame,
                              (0, 0),
                              (w, h),
                              f['flashcolor'],
                              4)
            scale = pipeline.defaults['font_scale'] - 0.1
            ret, baseline = cv2.getTextSize(
                f['text'],
                pipeline.defaults['font'],
                pipeline.defaults['font_scale'],
                pipeline.defaults['font_thickness'])
            textWidth = ret[0] + 6
            axis = (w - textWidth, h - 30)
            cv2.putText(frame,
                        f['text'],
                        axis,
                        pipeline.defaults['font'],
                        scale,
                        f['color'],
                        pipeline.defaults['font_thickness'])
            f['duration'] -= 1
