from typing import Tuple, List
import os
import numpy as np

import cv2
import face_recognition as facerec


def _face_profile(pipeline, face_encoding: List[np.ndarray]) -> Tuple[str, str, str]:
    # find the encoding in db and draw
    # face label in the same frame.
    # See if the face is a match for the known face(s) in db
    rows = pipeline.face_finder(face_encoding, 1)
    profile_id, name, file = None, pipeline.defaults['face_label'], None

    if rows is not None and len(rows) > 0:
        file, profile_id, profilename = rows[0]
        if profilename:
            name = profilename
        else:
            filename = os.path.basename(file)
            name = os.path.splitext(filename)[0]
            name = name.replace("_", " ").replace("-", " ")

    if len(name) > 16:
        name = name[0:16:] + '..'

    return profile_id, name, file, face_encoding


def _draw_labels(pipeline,
                 frame: np.ndarray,
                 profile: Tuple[str, str, str],
                 location: Tuple[float, float, float, float]):
    profile_id, name, file, face_encoding = profile
    top, right, bottom, left = location
    top *= 4
    right *= 4
    bottom *= 4
    left *= 4

    if pipeline.pipeline_counter['draw_faces'] == 0:
        face_crop = frame[top - 10:bottom + 10, left - 10: right + 10]
        if name == pipeline.defaults['face_label']:
            pipeline.hooks.face_not_found(face_crop, face_encoding)
        else:
            pipeline.hooks.face_found(face_crop, profile_id, name, file)

    # draw a box around the face
    cv2.rectangle(frame, (left, top), (right, bottom),
                  pipeline.defaults['rect_color'], 2)

    # Draw a label with a name below the face
    cv2.rectangle(frame, (left, bottom - 25),
                  (right, bottom),
                  pipeline.defaults['rect_color'],
                  cv2.FILLED)
    cv2.putText(frame,
                name,
                (left + 6, bottom - 6),
                pipeline.defaults['font'],
                pipeline.defaults['font_scale'],
                (255, 255, 255),
                pipeline.defaults['font_thickness'])


def draw_face_labels(pipeline,
                     frame: np.ndarray, w: int, h: int):

    # Resize frame of video to 1/4 size
    # for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses)
    # to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Find all the faces and face encodings in the current frame of video
    pipeline.face_locations = facerec.face_locations(rgb_small_frame)

    # only run thru face recognition
    # pipeline for every specified iteration
    pipeline.pipeline_counter['draw_faces'] += 1
    if pipeline.pipeline_counter['draw_faces'] == 5:
        pipeline.pipeline_counter['draw_faces'] = 0

        face_encodings = facerec.face_encodings(rgb_small_frame,
                                                pipeline.face_locations)
        pipeline.face_profiles = [_face_profile(
            pipeline, enc) for enc in face_encodings]

    # draw face labels
    for location, profile in zip(pipeline.face_locations, pipeline.face_profiles):
        _draw_labels(pipeline, frame, profile, location)
