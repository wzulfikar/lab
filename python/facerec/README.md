## Python Face Recognition with Postgres

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
python3 faceadd.py ./storage/photos/Barack_Obama_0001.jpg

# activate webcam
python3 facerec.py 0 ./postgres.sample.yml
```


#### Manually adding faces to profile 

1. get a profile ID from table `profiles` or create new one. let's assume that the ID is `35`
2. find faces from directory of images (or single image) using `facefind.py`, ie. `python3 facefind.py ~/photos`
3. new folder named `./facerec-faces` will be created in the directory you gave for `facefind.py` in step 2, ie. `~/photos/.facerec-faces`
4. go to the `.facerec-faces` directory and select the faces you wanted to add for the profile in one folder, ie. `newfaces-profile35`
5. use `faceadd.py <path> <profileid>` to add the faces: `python3 faceadd.py path-to/newfaces-profile35 35`