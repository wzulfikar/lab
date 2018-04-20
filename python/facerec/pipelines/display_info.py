import numpy as np
import cv2


class DisplayInfoPipeline:
    def __init__(self, pipeline_register):
        self.p_reg = pipeline_register
        self.process = self._display_info

    def _display_info(self, frame: np.ndarray, w: int, h: int,
                      args: tuple):
        fps_current, key_hints = args

        cv2.putText(frame,
                    self.p_reg.labels['up_since'],
                    (10, h - 10),
                    self.p_reg.defaults['font'],
                    self.p_reg.defaults['font_scale'] - 0.1,
                    (255, 255, 255),
                    self.p_reg.defaults['font_thickness'])

        if fps_current is not None:
            if fps_current > 0:
                cv2.putText(frame,
                            "{0:.1f} fps".format(fps_current),
                            (10, h - 25),
                            self.p_reg.defaults['font'],
                            self.p_reg.defaults['font_scale'] - 0.1,
                            (255, 255, 255),
                            self.p_reg.defaults['font_thickness'])
            else:
                cv2.putText(frame,
                            "calculating fps..".format(fps_current),
                            (10, h - 25),
                            self.p_reg.defaults['font'],
                            self.p_reg.defaults['font_scale'] - 0.1,
                            (255, 255, 255),
                            self.p_reg.defaults['font_thickness'])

        ret, baseline = cv2.getTextSize(
            key_hints,
            self.p_reg.defaults['font'],
            self.p_reg.defaults['font_scale'] - 0.1,
            self.p_reg.defaults['font_thickness'])
        textWidth = ret[0] + 6
        keyHintsAxis = (w - textWidth, h - 10)
        cv2.putText(frame,
                    key_hints,
                    keyHintsAxis,
                    self.p_reg.defaults['font'],
                    self.p_reg.defaults['font_scale'] - 0.1,
                    (255, 255, 255),
                    self.p_reg.defaults['font_thickness'])
