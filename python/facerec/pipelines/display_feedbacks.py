import numpy as np

import cv2


class DisplayFeedbacksPipeline:
    def __init__(self, pipeline_register):
        self.p_reg = pipeline_register
        self.process = self._display_feedbacks

    def _display_feedbacks(self,
                           frame: np.ndarray, w: int, h: int,
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
                scale = self.p_reg.defaults['font_scale'] - 0.1
                ret, baseline = cv2.getTextSize(
                    f['text'],
                    self.p_reg.defaults['font'],
                    self.p_reg.defaults['font_scale'],
                    self.p_reg.defaults['font_thickness'])
                textWidth = ret[0] + 6
                axis = (w - textWidth, h - 30)
                cv2.putText(frame,
                            f['text'],
                            axis,
                            self.p_reg.defaults['font'],
                            scale,
                            f['color'],
                            self.p_reg.defaults['font_thickness'])
                f['duration'] -= 1
