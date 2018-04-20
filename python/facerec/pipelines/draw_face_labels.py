from typing import Tuple, List
import os
import numpy as np

import cv2
import face_recognition as facerec


class DrawFaceLabelsPipeline:
    def __init__(self, pipeline_register):
        self.p_reg = pipeline_register
        self.process = self._draw_face_labels

    def _face_profile(self,
                      face_encoding: List[np.ndarray]) -> Tuple[str, str, str]:
        # find the encoding in db and draw
        # face label in the same frame.
        # See if the face is a match for the known face(s) in db
        rows = self.p_reg.face_finder(face_encoding, 1)
        profile_id, name, file = None, self.p_reg.defaults['face_label'], None

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

    def _draw_labels(self,
                     frame: np.ndarray,
                     profile: Tuple[str, str, str],
                     location: Tuple[float, float, float, float]):
        profile_id, name, file, face_encoding = profile

        # adjust the location to account rgb small frame
        top, right, bottom, left = location
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom),
                      self.p_reg.defaults['rect_color'], 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 25),
                      (right, bottom),
                      self.p_reg.defaults['rect_color'],
                      cv2.FILLED)
        cv2.putText(frame,
                    name,
                    (left + 6, bottom - 6),
                    self.p_reg.defaults['font'],
                    self.p_reg.defaults['font_scale'],
                    (255, 255, 255),
                    self.p_reg.defaults['font_thickness'])

    def _draw_face_labels(self, frame: np.ndarray, w: int, h: int):

        # Resize frame of video to 1/4 size
        # for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses)
        # to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Find all the faces and face encodings in the current frame of video
        self.p_reg.face_locations = facerec.face_locations(rgb_small_frame)

        # only run thru face recognition
        # pipeline for every specified iteration
        self.p_reg.pipeline_counter['draw_faces'] += 1
        if self.p_reg.pipeline_counter['draw_faces'] == 5:
            self.p_reg.pipeline_counter['draw_faces'] = 0

            face_encodings = facerec.face_encodings(rgb_small_frame,
                                                    self.p_reg.face_locations)
            self.p_reg.face_profiles = [self._face_profile(enc)
                                        for enc in face_encodings]

        # draw face labels
        # draw face labels
        update_presence = True
        for location, profile in zip(self.p_reg.face_locations,
                                     self.p_reg.face_profiles):
            if 'presence' in self.p_reg.pipelines:
                self.p_reg.pipelines['presence'].process(frame, w, h,
                                                         (update_presence,
                                                          location,
                                                          profile))
                update_presence = False

            self._draw_labels(frame, profile, location)
