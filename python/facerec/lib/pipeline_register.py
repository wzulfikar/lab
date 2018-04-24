from datetime import datetime
from typing import List

import cv2

from lib.pipeline_hooks import PipelineHooks
from pipelines.display_info import DisplayInfoPipeline
from pipelines.display_feedbacks import DisplayFeedbacksPipeline
from pipelines.draw_face_labels import DrawFaceLabelsPipeline
from pipelines.lookback import LookbackPipeline
from pipelines.presence import PresencePipeline
from pipelines.recorder import RecorderPipeline
from pipelines.key_press import KeyPressPipeline


class PipelineRegister:
    def __init__(self, pipelines: dict, hooks: dict, runtime_vars: dict):
        self.defaults = {
            'font': cv2.FONT_HERSHEY_DUPLEX,
            'font_scale': 0.5,
            'font_thickness': 1,
            'rect_color': (0, 0, 255),  # rgb red
        }

        self.runtime_vars = runtime_vars

        up_since = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.labels = {
            'up_since': "[FACEREC] UP SINCE {}".format(up_since)
        }

        # initialize pipelines
        print('initializing pipelines..')
        self.pipelines = {}
        self._init_pipelines(pipelines)

        # initialize pipeline hooks
        self.hooks = PipelineHooks(pipeline_register=self, hooks=hooks)


    def _init_pipelines(self, pipelines: dict):
        has_error = False
        for name, pipeline_args in pipelines.items():
            try:
                if type(pipeline_args) is not tuple:
                    fn = pipeline_args
                    self.pipelines[name] = fn(self)
                else:
                    fn, *args = pipeline_args
                    self.pipelines[name] = fn(self, *args)

                if not hasattr(self.pipelines[name], 'defer'):
                    self.pipelines[name].defer = False

                print('- pipeline {}: {}'.format(len(self.pipelines), name, fn))
            
            except TypeError as e:
                has_error = True
                print('[ERROR] failed to initialize pipeline "{}":'.format(name))
                print(e)

        if has_error:
            exit(1)

    def require(self, required_by: str, pipelines: List[str]):
        """
        ensure that given pipelines have been loaded.
        can be used by a pipeline that depends on other pipeline.
        """

        missing_dependencies = 0
        for pipeline in pipelines:
            if pipeline not in self.pipelines:
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

    def close_pipelines(self):
        print("- executing pipeline `closer` method..")
        for pipeline_name, pipeline in self.pipelines.items():
            if hasattr(pipeline, 'closer') and callable(getattr(pipeline, 'closer')):
                pipeline.closer()
                print("pipeline closed:", pipeline_name)