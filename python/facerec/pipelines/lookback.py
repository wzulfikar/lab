import numpy as np


class LookbackPipeline:
    def __init__(self, pipeline_register):
        self.p_reg = pipeline_register
        self.max_lookback_frames = 50
        self.frames = []

        self.process = self._append

    def _append(self, frame: np.ndarray):
        if len(self.frames) < self.max_lookback_frames:
            self.frames.append(frame)
        else:
            self.frames.pop(0)
