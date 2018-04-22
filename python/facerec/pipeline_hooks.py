from datetime import datetime
from typing import List
import os

import cv2
import numpy as np


class PipelineHooks:
    def __init__(self, pipeline_register):
        """handle face recognition events (hooks)"""

        self.p_reg = pipeline_register
        self.p_reg.require(self.__class__.__name__,
                           ['display_feedbacks'])

        self.display_feedbacks = self.p_reg.pipelines['display_feedbacks']

        self.storage = 'storage/hooks'
        if not os.path.exists(self.storage):
            os.mkdir(self.storage)

    def _timestamp(self):
        """helper method to create formatted timestmap"""
        return datetime.now().strftime('%Y-%m-%d_%H%M%S')

    def on_face_unknown(self,
                        face_crop: np.ndarray,
                        face_encoding: List[np.ndarray]):
        """triggered everytime an unknown face appears in frame"""

        self.display_feedbacks.display('unknown_face')

        print("[INFO] unknown face detected")
        filename = '{}/unknown_{}.jpg'.format(
            self.storage,
            self._timestamp())

        # only store the unknown face if it
        # comes from different time (seconds).
        cv2.imwrite(filename, face_crop)

    def on_face_appear(self,
                       face_crop: np.ndarray,
                       profile_id: str,
                       name: str,
                       file: str):
        """triggered everytime new face appears in frame"""

        self.display_feedbacks.display('on_enter',
                                       duration=30,
                                       fmt_args=(name))

        print("[PROFILE {}] face appears: {}, file: {}".format(
            profile_id, name, file))

    def on_face_disappear(self, profile_id: str, name: str):
        """triggered everytime a face disappears from frame"""

        self.display_feedbacks.display('on_leaving',
                                       duration=30,
                                       fmt_args=(name))

        print("[PROFILE {}] face disappears: {}".format(
            profile_id, name))

        # sample code to store last frame before someone leave
        # if 'lookback' in self.p_reg.pipelines:
        #     last_frame = self.p_reg.pipelines['lookback'].frames[-1]
        #     filename = '{}/before-leaving-{}-{}.jpg'.format(self.storage,
        #                                                     self._timestamp(),
        #                                                     name)
        #     cv2.imwrite(filename, last_frame)

    def on_all_leave(self, frame):
        """triggered when there's no face in frame"""
        self.display_feedbacks.display("whoops! all people leaves",
                                       duration=30)
        print("whoops! all people leaves")
