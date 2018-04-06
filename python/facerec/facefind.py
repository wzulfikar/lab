import os
import cv2
import sys
import dlib
import numpy
import postgresql
import face_recognition

if len(sys.argv) < 2:
    print("Usage: facefind <image>")
    exit(1)

if not os.path.exists("./.faces"):
    os.mkdir("./.faces")

print("Connecting to DB..")
db = postgresql.open('pq://user:pass@localhost:5434/db')
print("DB connected")

# Create a HOG face detector using the built-in dlib class
face_detector = dlib.get_frontal_face_detector()


def facelabel(img, name, rect, rect_color=(0, 0, 255)):
    left = rect.left()
    top = rect.top()
    right = rect.right()
    bottom = rect.bottom()

    cv2.rectangle(img,
                  (left, top),
                  (right, bottom),
                  rect_color,
                  1)
    # Draw a label with a name below the face
    cv2.rectangle(img,
                  (left, bottom - 25),
                  (right, bottom),
                  rect_color,
                  cv2.FILLED)
    cv2.putText(img, name,
                (rect.left() + 6, rect.bottom() - 6),
                cv2.FONT_HERSHEY_DUPLEX,
                0.5,
                (255, 255, 255),
                1)


def findface(db, enc) -> list:
    query = "SELECT file, split_part(p.name,' ',1) as name \
            FROM vectors  v \
            LEFT OUTER JOIN profiles p ON v.profile_id = p.id \
            ORDER BY " + \
            "(CUBE(array[{}]) <-> vec_low) + (CUBE(array[{}]) <-> vec_high) \
            ASC LIMIT 1".format(
                ','.join(str(s) for s in enc[0:63]),
                ','.join(str(s) for s in enc[64:127]),
            )
    return db.query(query)


def facerec(file_name):
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
        crop = img[face_rect.top():face_rect.bottom(),
                   face_rect.left():face_rect.right()]

        encodings = face_recognition.face_encodings(crop)
        if len(encodings) > 0:
            query = "SELECT file, split_part(p.name,' ',1) as name \
                        FROM vectors  v \
                        LEFT OUTER JOIN profiles p ON v.profile_id = p.id \
                        ORDER BY " + \
                    "(CUBE(array[{}]) <-> vec_low) + (CUBE(array[{}]) <-> vec_high) ASC LIMIT 1".format(
                        ','.join(str(s) for s in encodings[0][0:63]),
                        ','.join(str(s) for s in encodings[0][64:127]),
                    )
            rows = db.query(query)
            if len(rows) > 0:
                print(rows)
                file, profilename = rows[0]
                if profilename:
                    name = profilename
                else:
                    filename, ext = os.path.splitext(os.path.basename(file))
                    name = filename.replace("_", " ").replace("-", " ")

                facelabel(img, 'F.{}: {}'.format(i + 1, name), face_rect)
        else:
            facelabel(img, "F.{}".format(i + 1),
                      face_rect,
                      (0, 100, 255))

        filename, ext = os.path.splitext(os.path.basename(file_name))
        labeled_file = file_name.replace(ext, '_labeled{}'.format(ext))
        cv2.imwrite(labeled_file, img)

# Take the image(s) path from the command line
path = sys.argv[1]
if not os.path.exists(path):
    print("Path doesn't exist!", path)
    exit(1)

if os.path.isfile(path):
    print("Processing one file:", path)
    facerec(path)
else:
    print("Processing directory:", path)
    for root, dirs, files in os.walk(path):
        path = root.split(os.sep)
        for file in files:
            _, ext = os.path.splitext(file)
            if ext.lower() not in ['.jpg', '.jpeg']:
                print("[SKIP]", file)
                continue

            filepath = os.path.join(root, file)
            print("Image found: ", filepath)
            facerec(filepath)
