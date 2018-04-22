from datetime import datetime
from typing import List

import cv2

from pipeline_hooks import PipelineHooks
from pipelines.display_info import DisplayInfoPipeline
from pipelines.display_feedbacks import DisplayFeedbacksPipeline
from pipelines.draw_face_labels import DrawFaceLabelsPipeline
from pipelines.lookback import LookbackPipeline
from pipelines.presence import PresencePipeline
from pipelines.recorder import RecorderPipeline
from pipelines.key_press import KeyPressPipeline


class PipelineRegister:
    def __init__(self, pipelines: List[tuple]):
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
            'key_press': KeyPressPipeline,
        }

        # initialize pipelines
        print('initializing pipelines..')

        """initialize dict to store activated pipelines"""
        self.pipelines = {}
        self._initialize_pipelines(self.pipelines, self._p, pipelines)

        self.hooks = PipelineHooks(pipeline_register=self)

    def _initialize_pipelines(self,
                              pipelines_store: dict,
                              all_pipelines: dict,
                              chosen_pipelines: dict):
        for pipeline_args in chosen_pipelines:
            pipeline, args = None, []

            # extract pipeline name and its args
            if type(pipeline_args) is tuple:
                pipeline, *args = pipeline_args
            else:
                pipeline = pipeline_args

            if pipeline not in all_pipelines:
                print('[ERROR] invalid pipeline:', pipeline)
                exit(0)

            # initialize pipeline with its args (if any)
            errors = []
            try:
                if len(args) > 0:
                    pipelines_store[pipeline] = all_pipelines[pipeline](
                        self, *args)
                else:
                    pipelines_store[pipeline] = all_pipelines[pipeline](self)
            except TypeError as e:
                errors.append('{}: {}'.format(pipeline, e))

            if len(errors) > 0:
                print('failed to initialize pipelines:')
                for err in errors:
                    print(err)
                exit(1)

            print('- pipeline {}: {} ({} args)'.format(len(self.pipelines),
                                                       pipeline,
                                                       len(args)))

    def require(self, required_by: str, pipelines: List[str]):
        """
        ensure that given pipelines have been loaded.
        can be used by a pipeline that depends on other pipeline.
        """

        missing_dependencies = 0
        for pipeline in pipelines:
            if pipeline not in self._p:
                print('cannot require invalid pipeline:', pipeline)

            elif pipeline not in self.pipelines:
                print('[ERROR] {} has missing pipeline dependency: {}'.format(required_by,
                                                                              pipeline))
                missing_dependencies += 1

        if missing_dependencies > 0:
            print(
                """
failed to initialize pipelines:
make sure to load dependant pipelines after loading its dependencies.
""")
            exit(0)
