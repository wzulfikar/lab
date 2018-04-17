## Udacity Flying Car Nanodegree
> Sat, 14 Apr 2018 at 2:00:23 MYT

Preview link: https://classroom.udacity.com/courses/ud787-preview

Instructors:
1. Angle Schoelig, University of Toronto, Professor, Institute for Aerospace Studies
2. Nick Rocy, Professor of Aeronautics, MIT

### Lesson 2: Intro to Autonomous Flight

1. wright brothers: kitty hawk, north carolina
- the wright brothers did differently from previous aircraft designers in which the wright brothers designed the aircraft with adjustable wing shape (to imitate the flight of birds)
- first autopilot: 1912, by Sperry Corporation (Elmer Sperry). "autopilot": a system used to control the trajectory of an aircraft without *constant* 'hands-on' control by a human operator being required
- **quadrotors**: or quad, or drone with 4 rotors
- more drone (and autonomous drone) becomes possible because; 
    - cheaper microcontroller (ie. to perform in-flight data crunching tasks)
    - the availability of high-density battery that makes the quadrotor possible without traditional fuel (gas, oil, etc)
    - development of GPS (global positioning system). a small drone can now be outfitted with a gps system and give constant updates on its position
    - *summary*: powerful lightweight computer + battery + gps
- why use quadrotor to learn autonomous flight?
    - its symmetric simplicity makes understanding dynamics and control easier
    - it's the most accessible and affordable commercial vechicles, which makes it a great test platform to run code on real hardware
    - quadrator can perform VTOL (virtual take-off and landing) which is crucial to be able to operate in urban environment
    - summary: simplicity of design, accesibility & vtol

> **why a single rotor helicopter need to have single rotor in its tail?** *so the body doesn't spin together (out of control) with the rotor.* read more: angular momentum

#### Quadrotor Components
1. 4 rotors. each of 2 rotors that sits in one another spins in the same direction and hence, the two pairs of propellers on a quadrotor spin in opposite directions (the net torque from the two pairs of propellers cancel out so the vehicle is stable in flight)
2. motors (to move the rotors)
3. **inertial measurement unit (IMU)**: an electronic device that measures and reports a body's specific force, angular rate, and sometimes the magnetic field surrounding the body, using a combination of accelerometers and gyroscopes, sometimes also magnetometers.
4. battery
5. gps
6. camera
7. frame: a base where everything else is connected. should be strong but light

> Suppose your power supply has an operating range between 3-7 volts and to generate the appropriate amount of thrust for your quad (given it's weight, propeller size etc.) you need to achieve 15,000 RPMs when you're comfortably in the middle of the power supply's operating range. What's a good KV value for your motors?
> 
> **ans**: 3000 KV (the middle of our power supply range is 5. Kv = RPM/volt → 15000 / 5 → 3000)

#### More on Quadrotor Components

1. brushed vs brushless motor: http://www.quantumdev.com/brushless-motors-vs-brush-motors-whats-the-difference/
2. currently, battery technology is not as good as carbon-based fuels in delivering energy. and the way the electric motors convert energy to flight power is not as efficient as combustion engine. but, electric motor is the easiest to work with.
3. quadrotor use brushless motor so to spin faster and more efficient
4. **ESC (Electronic Speed Controller)**: tells motors how fast they should spin
5. `Kv = RPMs / volts`. Kv describes the RPMs that a motor will achieve (under zero load) when a given voltage is applied. ie, a motor that can do 4000 RPMs when 2 volts are applied gets a Kv rating of 2000 (4000 / 2 = 2000)
6. quadrotor has 2 clockwise rotors and 2 counter-clockwise rotors to allow zero-net torque
7. propeller has `radius` property. the bigger the radius, the slower the propeller will spin.
8. propeller also has `pitch` property (the *twist* of the propeller). formally, `pitch` is a linear distance where the propeller will move forward as a result of one rotation.
9. larger pitch props will move more air per revolution, and low pitch props (much flatter) to move lesser air per revolution
10. larger pitch is generally more efficient as it moves more air per revolution but it has lower thrust which make it less suitable for hovering in air. on the other hand, lower pitch has higher thrust which makes it suitable for hovering under heavy load (but they'd use up the battery more faster).
11. there are quadrotor that has *variable-pitch propeller* that can do low-pitch for hover and high-pitch for fast-forward motion. however, variable-pitch propeller is a lot more complicated. hence, you'd probably see fixed-pitch propellers more in drone.
12. battery used in quadrotor need to be able to discharge very quickly, which can be dangerous, compared to those batteries used in laptop or cellphone (although they use same battery technology, Lithium Polymer aka LiPo)
13. when picking battery, make sure that it has enough power to last comfortably during the mission, as well as bringing the payload
14. most of quadrotor power (from battery) goes to (consumed by) the motors
15. the quadrotor will hover when all the propellers spin fast enough to just bounce the gravity
16. the way you induce motion to quadrotor without it spinning uncontrollably is to increase the thrust on *adjacent* motors that spin on opposite direction
17. **euler angle**: three angles introduced by Leonhard Euler to describe the orientation of a rigid body with respect to a fixed coordinate system.
18. with all the tasks to control the thrusts in a quadrotor, manually controlling all four motors to fly the quad would be essentially impossible
19. autopilot adjust and control all the thrusts. however, it needs to know the control attitude of the vehicle. to do so, it uses information from the sensors: IMU (inertial measurement unit)
20. most IMU contains 3 gyroscopes and 3 accelerometers
21. accelerometer can tell us which way is down by referencing to gravity
22. **MEMS**: Micro Electro Mechanical System. it's a modern gyroscope to allow us to have an equivalent of 3 accelerometers and 3 gyroscopes into a tiny chip, ie. in smartphone
23. quadrotor can detect gps anomaly by combining datas from different sensors it has; barometer, IMU, camera, etc.
24. in quadrotor, a flight computer is equivalent to human brain (the one that controls the flight)
25. drone's **attitude control (autopilot) loop** (always running in the background):

    ```
      IMU    →  Autopilot
       ↑          ↓
    Vehicle  ←   Motors
    ```
26. drone's **position control loop**:

    ```
            GPS            →      Flight Computer
             ↑                           ↓
    attitude control loop  ←   Target Thrust Vector
    ```
27. the autopilot loop might be executed in 50 cycles per second (50hz) while the position loop might be executed in few times per seconds. the two loops doesn't necessarily need to be synchronized.

---


- building robot in human-centered environment is a challenge. it needs to be aware of its surroundings
- Sebastian Thrun: founder of Udacity, CEO of kitty hawk
- Flying Card Nanodegree (FCND) Simulator: https://github.com/udacity/FCND-Simulator-Releases
- conundrum: a confusing and difficult problem or question
