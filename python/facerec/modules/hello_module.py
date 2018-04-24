# sample module to play around with iris's module mechanism

import numpy as np


def hello(face_crop: np.ndarray,
          profile_id: str,
          name: str,
          file: str):
    """print greeting in console when a face appear"""
    print('Hello {}!'.format(name))

def hello_unknown(face_crop: np.ndarray,
          profile_id: str,
          name: str,
          file: str):
    print('Hello unknown! '.format(name))


def on_start():
    print('frame loop started!')

def on_stop():
    print('frame loop stopped!')
