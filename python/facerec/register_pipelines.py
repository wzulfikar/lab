import os 

# import pipeline register and event listeners
from lib.pipeline_register import PipelineRegister
import event_listeners

from pipelines.lookback import LookbackPipeline
from pipelines.display_info import DisplayInfoPipeline
from pipelines.display_feedbacks import DisplayFeedbacksPipeline
from pipelines.draw_face_labels import DrawFaceLabelsPipeline
from pipelines.lookback import LookbackPipeline
from pipelines.presence import PresencePipeline
from pipelines.recorder import RecorderPipeline
from pipelines.key_press import KeyPressPipeline
from modules.facerec.facerec_pg import FacerecPG

def register(conf: dict, runtime_vars: dict, video_capture):
    """register pipelines to be used by the application"""
    
    facerec = FacerecPG(conf['postgres'])
    storage = _prepare_storage({
        "screenshots": '{}/screenshots'.format(conf["storage"]),
        "recordings": '{}/recordings'.format(conf["storage"]),
    })
    
    # register your pipelines here
    pipelines = {
        'lookback': LookbackPipeline,
        'display_info': DisplayInfoPipeline,
        'display_feedbacks': DisplayFeedbacksPipeline,
        'draw_face_labels': (DrawFaceLabelsPipeline, facerec.findfaces),
        'presence': PresencePipeline,
        'recorder': (RecorderPipeline, video_capture,
                                       storage['recordings'],
                                       conf['frame']['recordonstart']),
        'key_press': (KeyPressPipeline, storage['screenshots']),
    }
    
    return PipelineRegister(pipelines, event_listeners.register(), runtime_vars)


def _prepare_storage(storage: dict):
    for key, path in storage.items():
        if not os.path.exists(path):
            print("- creating '{}' storage at {}".format(key, path))
            os.makedirs(path)

    return storage