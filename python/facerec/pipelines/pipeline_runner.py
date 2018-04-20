import os
from datetime import datetime
from typing import List, NamedTuple, Tuple
from concurrent.futures import ThreadPoolExecutor

import cv2
import numpy as np

from pipeline_hooks import PipelineHooks
from pipelines.display_info import display_info
from pipelines.display_feedbacks import display_feedbacks
from pipelines.draw_face_labels import draw_face_labels

print("- configuring environment..")

FaceProfile = Tuple[str, str, str, List[np.ndarray]]


class PipelineRunner:
    def __init__(self, face_finder):
        self.hooks = PipelineHooks()

        self.face_locations: List[tuple] = []
        self.face_profiles: List[FaceProfile] = []
        self.face_finder = face_finder

        self.defaults = {
            'face_label': 'Unknown',
            'font': cv2.FONT_HERSHEY_DUPLEX,
            'font_scale': 0.5,
            'font_thickness': 1,
            'rect_color': (0, 0, 255),  # rgb red
        }

        up_since = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.labels = {
            'up_since': "[FACEREC] UP SINCE {}".format(up_since)
        }

        self.pipeline_counter = {
            'draw_faces': 0
        }

        # register pipelines
        print('registering pipelines..')
        self.p = {
            'display_info': display_info,
            'display_feedbacks': display_feedbacks,
            'draw_face_labels': draw_face_labels,
        }

    def run(self, pipeline_name: str, *args):
        self.p[pipeline_name](self, *args)
