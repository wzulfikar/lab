## Udacity: Intro to Self-driving Car
> Sat, 14 Apr 2018 at 2:00:23 MYT

Preview link: https://classroom.udacity.com/courses/ud013-preview/lessons/ab5998f5-8d95-4604-a4a3-5246768986d8/concepts/f645ea5b-caeb-467f-ac45-3f7f835c38fc

### Lesson 4

- Sensor fusion focuses on combining data coming in from a vehicle's lidar and radar sensors in order to detect objects in the world around it.

##### LIDAR (Light Imaging Detection and Ranging)
- Used to detect objects on the surface as well as their size and exact disposition
- LIDAR uses laser light pulses to scan the environment as opposed to radio or sound waves
- LIDAR was invented by U.S military and NASA more than 45 years ago for measuring distance in space. first commercial usage occur on 1995 for topographical needs
- LIDAR algorithm in a nutshell:
    1. Emit laser signals
    2. Laser signals reach an obstacle
    3. Signal reflects from the obstacle
    4. Signal returns to the receiver
    5. A laser pulse is registered
- compared to sound waves, using LIDAR, the light is 1.000.000 times faster than the sound
- A LIDAR can build an exact 3D monochromatic image of an object
- Some disadvantages of using LIDAR:
    - Limited usage in nighttime/cloudy weather.
    - Operating altitude is only 500-2000m.
    - Quite an expensive technology.

##### RADAR (Radio Detection and Ranging)

- used to detect objects at a distance, define their speed and disposition
- invented in 1940, right before World War II; however, development actually started in 1886 when one German physicist realized that radio waves could reflect from solid objects.
- compared with LIDAR, RADAR uses radio waves instead of of light (the use of different signals to detect objects; light vs radio wave)
- RADAR can easily operate in cloudy weather conditions, and at night. It also has a longer operating distance.

> Articles on lidar vs radar: 
> 
- http://www.archer-soft.com/en/blog/lidar-vs-radar-comparison-which-system-better-automotive
- http://robotsforroboticists.com/lidar-vs-radar/


#### Kalman Filters

- a simpler sensor fusion technique (ie. combining data from LIDAR and RADAR)
- **extended kalman filter**: capable of handling more complex motion and measurement models

#### PID Control

- CTE: crosstrack error
- reference trajectory: represents a suggested path by which the controlled variable should converge on the set-point in a specified manner
- when driving a car, the program will steer in proportion to CTE. which means that the larger the error the more the vehicle will be turned toward reference trajectory
- larger CTE basically means that the vehicle is moving further away from reference trajectory

#### Model Predictive Control

- sliding window technique:
