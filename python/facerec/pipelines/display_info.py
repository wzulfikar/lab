import time

import numpy as np
import cv2


class DisplayInfoPipeline:
    def __init__(self, pipeline_register, runtime_vars: dict, key_hints: str):
        self.p_reg = pipeline_register
        self.process = self._display_info

        self.runtime_vars = runtime_vars
        self.key_hints = key_hints

        self.fps_time = time.time()
        self.frame_count = 0

    def _update_fps(self):
        seconds = time.time() - self.fps_time
        self.fps_time = time.time()
        self.runtime_vars['current_fps'] = self.frame_count / seconds
        print("- current fps:", self.runtime_vars['current_fps'])

        self.frame_count = 0

    def _display_info(self, frame: np.ndarray, w: int, h: int,
                      isrecording: bool):
        self.frame_count += 1

        if self.frame_count == 20:
            self._update_fps()

        cv2.putText(frame,
                    self.p_reg.labels['up_since'],
                    (10, h - 10),
                    self.p_reg.defaults['font'],
                    self.p_reg.defaults['font_scale'] - 0.1,
                    (255, 255, 255),
                    self.p_reg.defaults['font_thickness'])

        current_fps = self.runtime_vars['current_fps']
        if current_fps is not None:
            if current_fps > 0:
                cv2.putText(frame,
                            "{0:.1f} fps".format(current_fps),
                            (10, h - 25),
                            self.p_reg.defaults['font'],
                            self.p_reg.defaults['font_scale'] - 0.1,
                            (255, 255, 255),
                            self.p_reg.defaults['font_thickness'])
            else:
                cv2.putText(frame,
                            "calculating fps..".format(current_fps),
                            (10, h - 25),
                            self.p_reg.defaults['font'],
                            self.p_reg.defaults['font_scale'] - 0.1,
                            (255, 255, 255),
                            self.p_reg.defaults['font_thickness'])

        ret, baseline = cv2.getTextSize(
            self.key_hints,
            self.p_reg.defaults['font'],
            self.p_reg.defaults['font_scale'] - 0.1,
            self.p_reg.defaults['font_thickness'])
        textWidth = ret[0] + 6
        keyHintsAxis = (w - textWidth, h - 10)
        cv2.putText(frame,
                    self.key_hints,
                    keyHintsAxis,
                    self.p_reg.defaults['font'],
                    self.p_reg.defaults['font_scale'] - 0.1,
                    (255, 255, 255),
                    self.p_reg.defaults['font_thickness'])

        if isrecording:
            x, y = keyHintsAxis
            cv2.putText(frame,
                        '[R]',
                        (x - 23, y + 1),
                        self.p_reg.defaults['font'],
                        self.p_reg.defaults['font_scale'] - 0.1,
                        (0, 0, 255),  # rgb red
                        self.p_reg.defaults['font_thickness'])
