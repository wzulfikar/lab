from datetime import datetime
from typing import List
import os

import cv2
import numpy as np


class PipelineHooks:
    def __init__(self):
        """handle face recognition events (hooks)"""

        self.storage = 'storage/faces'
        if not os.path.exists(self.storage):
            os.mkdir(self.storage)

    def face_not_found(self,
                       face_crop: np.ndarray,
                       face_encoding: List[np.ndarray]):
        """triggered everytime unknown face is detected"""

        print("[INFO] unknown face detected")
        now = datetime.now()
        filename = '{}/unknown_{}.jpg'.format(
            self.storage,
            now.strftime('%Y-%m-%d_%H%M%S'))

        # only store the unknown face if it
        # comes from different time (seconds).
        if not os.path.exists(filename):
            cv2.imwrite(filename, face_crop)

    def face_found(self, face_crop, profile_id: int, name: str, file: str):
        """triggered everytime a known face is detected"""

        print("[PROFILE {}] face detected: {}, file: {}".format(
            profile_id, name, file))
