import os
from datetime import datetime
from typing import List, NamedTuple, Tuple
from concurrent.futures import ThreadPoolExecutor

import cv2
import numpy as np

from pipeline_hooks import PipelineHooks
from pipelines.display_info import DisplayInfoPipeline
from pipelines.display_feedbacks import DisplayFeedbacksPipeline
from pipelines.draw_face_labels import DrawFaceLabelsPipeline
from pipelines.lookback import LookbackPipeline
from pipelines.presence import PresencePipeline
from pipelines.recorder import RecorderPipeline

FaceProfile = Tuple[str, str, str, List[np.ndarray]]


class PipelineRegister:
    def __init__(self, face_finder, pipelines: list):
        self.hooks = PipelineHooks(pipeline_register=self)

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
            'draw_faces': 0,
        }

        # store all available pipelines
        self._p = {
            'display_info': DisplayInfoPipeline,
            'display_feedbacks': DisplayFeedbacksPipeline,
            'draw_face_labels': DrawFaceLabelsPipeline,
            'lookback': LookbackPipeline,
            'presence': PresencePipeline,
            'recorder': RecorderPipeline,
        }

        # register pipelines
        print('registering pipelines..')

        """initialize dict to store activated pipelines"""
        self.pipelines = {}

        counter = 0
        for pipeline in pipelines:
            if pipeline not in self._p:
                print('[ERROR] invalid pipeline:', pipeline)
                exit(0)

            counter += 1
            self.pipelines[pipeline] = self._p[pipeline](pipeline_register=self)
            print('- pipeline {}: {}'.format(counter, pipeline))
