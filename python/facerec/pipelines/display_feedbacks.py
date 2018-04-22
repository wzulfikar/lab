import numpy as np

import cv2


class DisplayFeedbacksPipeline:
    def __init__(self,
                 pipeline_register,
                 feedbacks: dict,
                 default_duration: int):
        self.p_reg = pipeline_register
        self.default_duration = default_duration
        self.feedbacks = feedbacks

        self._active_feedbacks = 0

        self.process = self._display_feedbacks

        self.feedback_tpl = {
            'text': "your text here",
            'duration': 0,
            'color': (0, 0, 255),  # bgr red
            'flashcolor': None,
        }

    def display(self, feedback_name: str,
                duration: int = None,
                fmt_args: tuple = None,
                bgr_color: tuple = None):
        if feedback_name not in self.feedbacks:
            self.feedbacks[feedback_name] = self.feedback_tpl
            self.feedbacks[feedback_name]['text'] = feedback_name

        if bgr_color is not None:
            self.feedbacks[feedback_name]['color'] = bgr_color

        if duration is None:
            duration = self.default_duration

        if fmt_args is not None:
            self.feedbacks[feedback_name]['args'] = fmt_args

        self.feedbacks[feedback_name]['duration'] = duration

    def _display_text(self, frame, w: int, h: int,
                      text: str,
                      color: tuple,
                      fmt_args: tuple):
        if fmt_args is not None:
            text = text.format(fmt_args)

        scale = self.p_reg.defaults['font_scale'] - 0.1
        ret, baseline = cv2.getTextSize(
            text,
            self.p_reg.defaults['font'],
            scale,
            self.p_reg.defaults['font_thickness'])
        textWidth = ret[0] + 6
        textHeight = ret[1] + 6

        axis = (w - textWidth, h - 30 - (textHeight * self._active_feedbacks))

        cv2.putText(frame,
                    text,
                    axis,
                    self.p_reg.defaults['font'],
                    scale,
                    color,
                    self.p_reg.defaults['font_thickness'])

    def _display_feedbacks(self, frame: np.ndarray, w: int, h: int):
        # display feedback frames
        for i, f in self.feedbacks.items():
            if f['duration']:
                if f['flashcolor']:
                    cv2.rectangle(frame,
                                  (0, 0),
                                  (w, h),
                                  f['flashcolor'],
                                  4)
                self._display_text(frame, w, h,
                                   f['text'],
                                   f['color'],
                                   f['args'] if 'args' in f else None)
                self._active_feedbacks += 1
                f['duration'] -= 1
            else:
                if self._active_feedbacks > 0:
                    self._active_feedbacks -= 1
