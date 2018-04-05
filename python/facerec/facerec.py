# a mashup of facerec_from_webcam_faster.py 
# from https://github.com/ageitgey/face_recognition
# and `face-postgre` from https://github.com/vearutop/face-postgre

import os
import cv2
import sys
import yaml
import dlib
import numpy
import postgresql
import face_recognition

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

if len(sys.argv) < 3:
	print("USAGE : facerec <source> <dbconfig>")
	print("SAMPLE: facerec 0 ./postgresql.sample.yml")
	print("        facerec http://example.com/axis-cgi/mjpg/video.cgi?camera=3 ./postgresql.sample.yml")
	exit(1)

if not os.path.exists("./.faces"):
	os.mkdir("./.faces")

# Create a HOG face detector using the built-in dlib class
face_detector = dlib.get_frontal_face_detector()

# Initialize some variables
default_name = "Unknown"
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

class facerec:
	def __init__(self, config: str):
		self.dbconf = yaml.safe_load(open(config))
		self.db = postgresql.open('pq://{}:{}@{}:{}/{}'.format(
			self.dbconf['user'],
			self.dbconf['pass'],
			self.dbconf['host'],
			self.dbconf['port'],
			self.dbconf['db']))

	def findface(self, enc: numpy.ndarray) -> list:
		query = "SELECT file, split_part(p.name,' ',1) as name FROM vectors  v left outer join profiles p on v.profile_id = p.id ORDER BY " + \
				"(CUBE(array[{}]) <-> vec_low) + (CUBE(array[{}]) <-> vec_high) ASC LIMIT 1".format(
			','.join(str(s) for s in enc[0:63]),
			','.join(str(s) for s in enc[64:127]),
		)
		return self.db.query(query)

class facerecvideo:
	def __init__(self, source: str):
		if source.isdigit():
			self.capture, self.info = cv2.VideoCapture(int(0)), "<device {}>".format(source)
		else:
			self.capture, self.info = cv2.VideoCapture(source), "<{}>".format(source)

frvideo = facerecvideo(sys.argv[1])
print("- Using video at "+frvideo.info)

fr = facerec(sys.argv[2])
print("- Using DB at {}:{}/{}".format(fr.dbconf['host'], fr.dbconf['port'], fr.dbconf['db']))


print("setting up facerec..")
FONT = cv2.FONT_HERSHEY_DUPLEX
FONT_SCALE = 0.5
FONT_THICKNESS = 1
RECT_COLOR = (0, 0, 255) # red
print("facerec is activated")

while True:
	# Grab a single frame of video
	ret, frame = frvideo.capture.read()

	# Resize frame of video to 1/4 size for faster face recognition processing
	small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

	# Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
	rgb_small_frame = small_frame[:, :, ::-1]

	# Only process every other frame of video to save time
	if process_this_frame:
		# Find all the faces and face encodings in the current frame of video
		face_locations = face_recognition.face_locations(rgb_small_frame)
		face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

		face_names = []
		for face_encoding in face_encodings:
			# See if the face is a match for the known face(s) in db
			rows = fr.findface(face_encoding)
			if len(rows) == 0:
				name = default_name
			else:			
				file, profilename = rows[0]
				if profilename:
					name = profilename
				else:
					filename = os.path.basename(file)
					name = os.path.splitext(filename)[0]
					name = name.replace("_", " ").replace("-", " ")
		
			face_names.append(name)
			print("face detected: "+name)

	process_this_frame = not process_this_frame

	# Display the results
	for (top, right, bottom, left), name in zip(face_locations, face_names):
		# Scale back up face locations since the frame we detected in was scaled to 1/4 size
		top *= 4
		right *= 4
		bottom *= 4
		left *= 4

		# Draw a box around the face
		cv2.rectangle(frame, (left, top), (right, bottom), RECT_COLOR, 2)

		# Draw a label with a name below the face
		cv2.rectangle(frame, (left, bottom - 25), (right, bottom), RECT_COLOR, cv2.FILLED)
		cv2.putText(frame, name, (left + 6, bottom - 6), FONT, FONT_SCALE, (255, 255, 255), FONT_THICKNESS)

	# Display the resulting image
	cv2.imshow('Video source: '+frvideo.info, frame)

	# Hit 'q' on the keyboard to quit!
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# Release handle to the webcam
frvideo.capture.release()
cv2.destroyAllWindows()

print("[EXIT] facerec exited")
