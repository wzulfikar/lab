import numpy as np

import cv2

BGR_WHITE = (255, 255, 255)
BGR_LIME = (0, 255, 0)
BGR_RED = (0, 0, 255)

DEFAULT_FEEDBACKS = {
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

# feedback duration in frames
DEFAULT_FEEDBACK_DURATION = 7


class DisplayFeedbacksPipeline:
    def __init__(self,
                 pipeline_register,
                 feedbacks: dict = None,
                 default_duration: int = None):
        self.p_reg = pipeline_register
        
        self.default_duration = default_duration
        if self.default_duration is None:
            self.default_duration = DEFAULT_FEEDBACK_DURATION
        
        self.feedbacks = feedbacks
        if self.feedbacks is None:
            self.feedbacks = DEFAULT_FEEDBACKS

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


    def _display_feedbacks(self, frame: np.ndarray):
        w = self.p_reg.runtime_vars['framewidth']
        h = self.p_reg.runtime_vars['frameheight']
        # display feedback frames
        for i, f in self.feedbacks.items():
            if f['duration']:
                if f['flashcolor']:
                    cv2.rectangle(frame, (0, 0), (w, h), f['flashcolor'], 4)
                
                self._display_text(frame, w, h, f['text'], f['color'],
                                   f['args'] if 'args' in f else None)
                self._active_feedbacks += 1
                f['duration'] -= 1
            else:
                if self._active_feedbacks > 0:
                    self._active_feedbacks -= 1

