## Udacity: Intro to Self-driving Car
> Sat, 27 Apr 2018 at 2:00:23 MYT

Preview link: https://classroom.udacity.com/courses/ud013-preview/lessons/06715629-363d-476c-b286-50909c109a3c/concepts/d8d00d85-38cb-45b8-b4f8-a511b535174e

### Lesson 5

- overall flow of data in self driving car, operating from fastest time (frequent update) to slowest:
    1. motion control (updated most frequently)
    2. sensor fusion
    3. localization and trajectory
    4. prediction
    5. behavior planning (lowest update rate)
- behavior planning get inputs from localization and precition. the output of behavior planning will then be used by trajectory which then passed to motion control (think of loopback)
- **finite state machine**: a technique to implement behavior planner 
- **cost function**: used to make behavior level decision
- **semantic segmentation**: the task of assigning meaning to part of an object
- semantic segmentation helps us to derive valuable information about every pixel in the image
- **scene understanding**: in contrast to object recognition, it attempts to analyze objects in context with respect to the 3D structure of the scene, its layout, and the spatial, functional, and semantic relationships between objects.
- **Functional Safety**: reducing risk in electronic systems (ISO 26262)
- **waypoints**: ordered set of coordinates that vehicle uses to plan a path around the track
- **Carla**: udacity's self-driving car
- **ROS framework**: Robot Operating System (ROS) framework, ie. collection of software frameworks for robot software development (hardware abstraction, low-level device control, etc.)
