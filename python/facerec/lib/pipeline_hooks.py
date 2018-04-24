from datetime import datetime
from typing import List
import os
from logging import debug

import cv2
import numpy as np


class PipelineHooks:
    def __init__(self, pipeline_register, hooks):
        """handle face recognition events (hooks)"""

        self.p_reg = pipeline_register
        self.p_reg.require(self.__class__.__name__,
                           ['display_feedbacks'])

        self.hooks = hooks
        self._validate_hooks()

        self.display_feedbacks = self.p_reg.pipelines['display_feedbacks']

        self.storage = 'storage/hooks'
        if not os.path.exists(self.storage):
            os.mkdir(self.storage)

    def _validate_hooks(self):
        print("validating hooks..")
        invalid_hooks = []
        for hook_name, listeners in self.hooks.items():
            if hasattr(self, hook_name) and callable(getattr(self, hook_name)):
                print('- {}: {}'.format(hook_name, listeners))
                continue
            else:
                invalid_hooks.append(hook_name)

        if len(invalid_hooks) > 0:
            print('[ERROR] invalid hooks:', invalid_hooks)
            exit(1)

    def _run_hooks(self, fn, *args):
        debug('running hooks for ', fn)
        for fn_name, listeners in self.hooks.items():
            if fn_name == fn:
                for listener in listeners:
                    debug('- listener called:', listener)
                    if args is None:
                        listener()
                    else:
                        listener(*args)

    def _timestamp(self):
        """helper method to create formatted timestmap"""
        return datetime.now().strftime('%Y-%m-%d_%H%M%S')

    def on_start(self):
        """triggered when the frame loop has started"""
        self._run_hooks('on_start')

    def on_stop(self):
        """triggered when the frame loop has stopped"""
        self._run_hooks('on_stop')

    def on_face_unknown(self,
                        face_crop: np.ndarray,
                        face_encoding: List[np.ndarray]):
        """triggered everytime an unknown face appears in frame"""
        self._run_hooks('on_face_unknown', face_crop, face_encoding)

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
        self._run_hooks('on_face_appear', face_crop, profile_id, name, file)
        self.display_feedbacks.display('on_enter',
                                       duration=30,
                                       fmt_args=(name))

        print("[PROFILE {}] face appears: {}, file: {}".format(
            profile_id, name, file))

    def on_face_disappear(self, profile_id: str, name: str):
        """triggered everytime a face disappears from frame"""
        self._run_hooks('on_face_disappear', profile_id, name)

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
        self._run_hooks('on_all_leave', frame)

        self.display_feedbacks.display("whoops! all people leaves",
                                       duration=30)
        print("whoops! all people leaves")
