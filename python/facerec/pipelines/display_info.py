import time

import numpy as np
import cv2


DEFAULT_KEY_HINTS = "q: quit, r: record, s: screenshot, v or h: flip"

class DisplayInfoPipeline:
    def __init__(self, 
                 pipeline_register, 
                 key_hints: str = None):
        self.p_reg = pipeline_register
        
        self.process = self._display_info

        self._recorder = None
        if 'recorder' in self.p_reg.pipelines:
            self._recorder = self.p_reg.pipelines['recorder']
        else:
            print('recorder pipeline not detected: recording indicator will not be displayed')
        
        self.key_hints = key_hints
        if self.key_hints is None:
            self.key_hints = DEFAULT_KEY_HINTS
            
        self.fps_time = time.time()
        self.frame_count = 0

    def _update_fps(self):
        seconds = time.time() - self.fps_time
        self.fps_time = time.time()
        self.p_reg.runtime_vars['current_fps'] = self.frame_count / seconds
        print("- current fps:", self.p_reg.runtime_vars['current_fps'])

        self.frame_count = 0

    def _display_info(self, frame: np.ndarray):
        self.frame_count += 1

        if self.frame_count == 20:
            self._update_fps()

        cv2.putText(frame,
                    self.p_reg.labels['up_since'],
                    (10, self.p_reg.runtime_vars['frameheight'] - 10),
                    self.p_reg.defaults['font'],
                    self.p_reg.defaults['font_scale'] - 0.1,
                    (255, 255, 255),
                    self.p_reg.defaults['font_thickness'])

        current_fps = self.p_reg.runtime_vars['current_fps']
        if current_fps is not None:
            if current_fps > 0:
                cv2.putText(frame,
                            "{0:.1f} fps".format(current_fps),
                            (10, self.p_reg.runtime_vars['frameheight'] - 25),
                            self.p_reg.defaults['font'],
                            self.p_reg.defaults['font_scale'] - 0.1,
                            (255, 255, 255),
                            self.p_reg.defaults['font_thickness'])
            else:
                cv2.putText(frame,
                            "calculating fps..".format(current_fps),
                            (10, self.p_reg.runtime_vars['frameheight'] - 25),
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
        keyHintsAxis = (self.p_reg.runtime_vars['framewidth'] - textWidth, 
                        self.p_reg.runtime_vars['frameheight'] - 10)
        cv2.putText(frame,
                    self.key_hints,
                    keyHintsAxis,
                    self.p_reg.defaults['font'],
                    self.p_reg.defaults['font_scale'] - 0.1,
                    (255, 255, 255),
                    self.p_reg.defaults['font_thickness'])

        if self._recorder and self._recorder.isrecording:
            x, y = keyHintsAxis
            cv2.putText(frame,
                        '[R]',
                        (x - 23, y + 1),
                        self.p_reg.defaults['font'],
                        self.p_reg.defaults['font_scale'] - 0.1,
                        (0, 0, 255),  # rgb red
                        self.p_reg.defaults['font_thickness'])
