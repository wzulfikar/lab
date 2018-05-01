## Udacity: Intro to Self-driving Car
> Sat, 14 Apr 2018 at 2:00:23 MYT

Preview link: https://classroom.udacity.com/courses/ud013-preview/lessons/631bcee2-d6bf-49a9-a2a9-168214e8d278/concepts/e19213bb-bf3e-4d16-aa8d-fe80d5e008f1

### Lesson 3

#### Deep Learning

- neural network: machine learning algorithm that you can train using input like camera, sensor, etc. and generate output
- the idea of neural network is that it learns from observing the world, we don't have to teach it anythin specific 
- deep learning: a term that describes big multi-layer neural network. it's also a term for using deep neural network to solve a problem.
- deep learning is relatively new, until the last few years where computer simply works fast enough to train deep neural network effectively. and with that, automotive manufacture can apply deep learning technique to drive a car in real time

#### Tracking Pipeline

1. in tracking pipeline, we'll run a search for a car in each frame of video using sliding window technique
- in the case of overlapping detection when doing sliding window technique, the center of overlapping window will be taken as the object
- in sliding window technique, we identify false positive detection by checking if it only appears in one frame (and not the next frame)
- adding **high covenance detection** will give us ability to detect how a center of overlap (a center of object) is moving from time to time and eventually estimate when it will appear in each subsequent frame (aka. predict where the object will be)
