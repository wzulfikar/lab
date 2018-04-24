import os
import cv2
import sys
import dlib
import postgresql
import face_recognition

import numpy as np

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import db

description = "find face from image and optionally add label"
usage = "usage: facefind <image> --addlabel"

def command(args):
    if len(args) < 2:
        print('facefind:', description)
        print(usage)
        exit(1)

    main(*args)


def main(path: str, maybe_addlabel: str = None):
    if not os.path.exists("./.faces"):
        os.mkdir("./.faces")

    if not os.path.exists(path):
        print("image doesn't exist:", path)
        exit(1)

    addlabel = maybe_addlabel == '--addlabel'
    if addlabel:
        print("addlabel option has been enabled")

    if os.path.isfile(path):
        print("Processing one file:", path)
        _facerec(path, addlabel)
        return

    print("Processing directory:", path)
    for root, dirs, files in os.walk(path):
        path = root.split(os.sep)

        currentdir = os.path.basename(root)
        if len(currentdir) > 1 and currentdir == '.':
            print("[SKIP] hidden directory:", currentdir)

        for file in files:
            _, ext = os.path.splitext(file)
            if ext.lower() not in ['.jpg', '.jpeg', '.png']:
                print("[SKIP]", file)
                continue

            filepath = os.path.join(root, file)
            print("Image found: ", filepath)
            _facerec(filepath, addlabel)

    db_conn = db.open()
    _findface(db_conn)


def _facelabel(img: np.ndarray, name: str, rect, rect_color=(0, 0, 255)):
    left = rect.left()
    top = rect.top()
    right = rect.right()
    bottom = rect.bottom()

    cv2.rectangle(img,
                  (left, top),
                  (right, bottom + 10),
                  rect_color,
                  2)

    # Draw a label with a name below the face
    cv2.rectangle(img,
                  (left, bottom - 15),
                  (right, bottom + 10),
                  rect_color,
                  cv2.FILLED)
    cv2.putText(img, name,
                (rect.left() + 6, rect.bottom() + 5),
                cv2.FONT_HERSHEY_DUPLEX,
                0.6,
                (255, 255, 255),
                1)


def _findface(db, enc) -> list:
    query = "SELECT file, p.name as name, p.id as profile_id \
            FROM vectors  v \
            LEFT OUTER JOIN profiles p ON v.profile_id = p.id \
            ORDER BY " + \
            "(CUBE(array[{}]) <-> vec_low) + (CUBE(array[{}]) <-> vec_high) \
            ASC LIMIT 1".format(
                ','.join(str(s) for s in enc[0:63]),
                ','.join(str(s) for s in enc[64:127]),
            )
    return db.query(query)


def _facerec(db, file_name, addlabel=None):
    path = os.path.dirname(file_name)
    imgname, ext = os.path.splitext(os.path.basename(file_name))

    facerecfaces = path + '/.facerec-faces'
    if not os.path.exists(facerecfaces):
        os.makedirs(facerecfaces)

    # Load the image
    img = cv2.imread(file_name)

    # Run the HOG face detector on the image data
    detected_faces = face_detector(img, 1)

    print("Found {} faces in the image file {}".format(
        len(detected_faces), file_name))

    # Loop through each face we found in the image
    for i, face_rect in enumerate(detected_faces):
        # Detected faces are returned as an object with the coordinates
        # of the top, left, right and bottom edges
        print("- Face #{} found at Left: {} Top: {} Right: {} Bottom: {}".format(i + 1, face_rect.left(), face_rect.top(),
                                                                                 face_rect.right(), face_rect.bottom()))
        crop = img[face_rect.top() - 10:face_rect.bottom() + 10,
                   face_rect.left() - 10: face_rect.right() + 10]

        label = 'F.{}-{}'.format(i + 1, 'Unknown')
        rect_color = (0, 0, 255)

        encodings = face_recognition.face_encodings(crop)
        if len(encodings) > 0:
            query = "SELECT file, p.name as name \
                        FROM vectors  v \
                        LEFT OUTER JOIN profiles p ON v.profile_id = p.id \
                        ORDER BY " + "(CUBE(array[{}]) <-> vec_low) + (CUBE(array[{}]) <-> vec_high) ASC LIMIT 1".format(
                    ','.join(str(s) for s in encodings[0][0:63]),
                    ','.join(str(s) for s in encodings[0][64:127]),
            )
            rows = db.query(query)
            if len(rows) > 0:
                print(' ', rows)
                file, profilename = rows[0]
                if profilename:
                    name = profilename
                else:
                    filename, ext = os.path.splitext(os.path.basename(file))
                    name = filename.replace("_", " ").replace("-", " ")

                label = label.replace('Unknown', name.replace(' ', '_'))
        else:
            print("  [SKIP] face has no encodings".format(i + 1)),
            rect_color = (0, 100, 255)

        cv2.imwrite('{}/{}{}'.format(facerecfaces,
                                     imgname + '-' + label, ext), crop)
        filename = os.path.splitext(os.path.basename(file_name))[0]

        if addlabel:
            if len(label) > 16:
                label = label[0:16:] + '..'
            print("- Adding face-label to image")
            facelabel(img, label.replace('_', ' '), face_rect, rect_color)
            cv2.imwrite('{}/{}_labeled{}'.format(path, filename, ext), img)

