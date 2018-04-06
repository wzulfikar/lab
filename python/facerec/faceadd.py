import sys
import dlib
import cv2
import face_recognition
import os
import postgresql
import time

if len(sys.argv) < 2:
    print("Usage: face-add <image>")
    exit(1)


def faceadd(db, face_detector, file_name):

    # Load the image
    image = cv2.imread(file_name)
    detected_faces = None

    try:
        # Run the HOG face detector on the image data
        detected_faces = face_detector(image, 1)
        print("Found {} faces in the image file {}".format(
            len(detected_faces), file_name))
    except RuntimeError:
        print("[ERROR] failed to detect face", file_name)
        return False

    if not os.path.exists("./.faces"):
        os.mkdir("./.faces")

    # Loop through each face we found in the image
    for i, face_rect in enumerate(detected_faces):
        # Detected faces are returned as an object with the coordinates
        # of the top, left, right and bottom edges
        print("- Face #{} found at Left: {} Top: {} Right: {} Bottom: {}".format(i, face_rect.left(), face_rect.top(),
                                                                                 face_rect.right(), face_rect.bottom()))
        crop = image[face_rect.top():face_rect.bottom(),
                     face_rect.left():face_rect.right()]
        encodings = face_recognition.face_encodings(crop)

        if len(encodings) > 0:
            query = "INSERT INTO vectors (file, vec_low, vec_high) VALUES ('{}', CUBE(array[{}]), CUBE(array[{}]))".format(
                file_name,
                ','.join(str(s) for s in encodings[0][0:63]),
                ','.join(str(s) for s in encodings[0][64:127]),
            )
            try:
                db.execute(query)
            except:
                print("[ERROR] failed to execute query", file_name)
                return False

        cv2.imwrite(
            "./.faces/aligned_face_{}_{}_crop.jpg".format(file_name.replace('/', '_'), i), crop)


# Take the image(s) path from the command line
path = sys.argv[1]

start = time.time()
if not os.path.exists(path):
    print("Path doesn't exist:", path)
    exit(1)

# Create a HOG face detector using the built-in dlib class
face_detector = dlib.get_frontal_face_detector()
db = postgresql.open('pq://user:pass@localhost:5434/db')
filecount = 0

if os.path.isfile(path):
    print("Processing single file:", path)
    faceadd(db, face_detector, path)
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
            print("[FOUND] ", filepath)
            if faceadd(db, face_detector, filepath) is not False:
                filecount += 1
                print("[DONE] File #{} added: {}".format(filecount, filepath))

print("Files processed:", filecount)
print("Time elapsed:", time.time() - start)
