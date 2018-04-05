A mashup of facerec_from_webcam_faster.py 
from https://github.com/ageitgey/face_recognition
and `face-postgre` from https://github.com/vearutop/face-postgre

```
# install dependencies
pip3 install py-postgresql face_recognition opencv-python

# start PostgreSQL 9.6 in docker (or use your natively)
docker-compose up -d

# initialize DB
python3 db.py

# adding face to db:
# this will extract face encodings (numpy.ndarray) from 
# given image and store the encodings in postgres db.
python3 face-add.py ./lfw/Barack_Obama_0001.jpg

# activate webcam
python3 facerec.py 0 ./postgres.sample.yml
```
