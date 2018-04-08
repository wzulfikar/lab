import sys
import dlib
import cv2
import face_recognition
import os
import postgresql
import time

if len(sys.argv) < 2:
    print("Usage: face-add <image> <profile_id (optional)>")
    exit(1)

PREVIEW_WINDOW = 'FaceAdd Preview'
cv2.namedWindow(PREVIEW_WINDOW, cv2.WINDOW_NORMAL)


def preview(windowname, img, label):
    preview = img
    cv2.putText(preview,
                label,
                (10, 25),
                cv2.FONT_HERSHEY_DUPLEX,
                0.5,
                (0, 0, 255),
                1)
    cv2.imshow(windowname, preview)
    cv2.waitKey(1)


def faceadd(db, face_detector, file_name, to_profile_id=None):
    promptprofile = False

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
        profile_id = to_profile_id

        # Detected faces are returned as an object with the coordinates
        # of the top, left, right and bottom edges
        print("- Face #{} found: at Left: {} Top: {} Right: {} Bottom: {}".format(i + 1, face_rect.left(), face_rect.top(),
                                                                                  face_rect.right(), face_rect.bottom()))
        crop = image[face_rect.top():face_rect.bottom(),
                     face_rect.left():face_rect.right()]
        encodings = face_recognition.face_encodings(crop)

        if not len(encodings):
            print("  [SKIP] face has no encodings")
        else:
            if not profile_id:
                insertprofile = None
                while(insertprofile is None):
                    previewimg = image[face_rect.top() - 25:face_rect.bottom() + 25,
                                       face_rect.left() - 25:face_rect.right() + 25]
                    preview(PREVIEW_WINDOW, previewimg, 'F.{}'.format(i + 1))
                    insertprofile = input(
                        "> Insert profile ID for face #{} (press enter to skip): ".format(i + 1))
                    if insertprofile != "":
                        profile_id = insertprofile

            print("- Adding face #{} to profile <{}>".format(i + 1, profile_id))
            if not profile_id:
                query = "INSERT INTO vectors (file, vec_low, vec_high) VALUES ('{}', CUBE(array[{}]), CUBE(array[{}]))".format(
                    file_name,
                    ','.join(str(s) for s in encodings[0][0:63]),
                    ','.join(str(s) for s in encodings[0][64:127]),
                )
            else:
                query = "INSERT INTO vectors (profile_id, file, vec_low, vec_high) VALUES ({}, '{}', CUBE(array[{}]), CUBE(array[{}]))".format(
                    profile_id,
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
    print("Path doesn't exist!", path)
    exit(1)

# Create a HOG face detector using the built-in dlib class
face_detector = dlib.get_frontal_face_detector()
db = postgresql.open('pq://user:pass@localhost:5434/db')
filecount = 0

profile_id = None
if len(sys.argv) > 2:
    profile_id = sys.argv[2]

if os.path.isfile(path):
    filecount += 1
    print("Processing single file:", path)
    faceadd(db, face_detector, path, profile_id)
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
            if faceadd(db, face_detector, filepath, profile_id) is not False:
                filecount += 1
                print("[DONE] File #{} added: {}".format(filecount, filepath))

cv2.destroyAllWindows()

print("Files processed:", filecount)
print("Time elapsed:", time.time() - start)
