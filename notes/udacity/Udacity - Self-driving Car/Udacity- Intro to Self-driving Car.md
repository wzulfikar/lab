## Udacity: Intro to Self-driving Car
> Sat, 14 Apr 2018 at 2:00:23 MYT

Preview link: https://classroom.udacity.com/courses/nd113-preview

### Lesson 2: Probability Preview
1. Localization: determining where a self-driving car is in the world
- the mathematical framework to get information is called statistic. bayes is the core of statistics. 
- statistic vs probability:
    - statistic: give data to find causes
    - probability: give causes to find data
- statistics & probability: a language to find relationship between data and causes
- P notation of fair coin: `P(heads)` → read: probability of the coin of coming up heads
- probability starts from 0 to 1 (float number)
- example of probability of fair coin:
    - `P(heads)`: 0.5 (50% chance to come up heads)
    - `P(tails)`: 0.5 (50% chance to come up tails)
- `P(A)`: `A` means complimentary outcomes of a probability
    - `P(A) = 1 - P(¬A)` (`¬A` means opposite event)
- composite event: `P.P...P` (independence)
- A self-driving car makes hundreds of calculations about probabilistic events every second, but the events are not as clean as a coin flip, ie:
    - *What is the probability that this sensor measurement is accurate to within 5 centimeters?*
    - *What is the probability that some other vehicle will turn left at this intersection? Go straight? Turn right?*
    - *The radar and lidar measurements seem to disagree! What's the probability that the range finder somehow became detached from the roof?*
- "In fact, humans drive (reasonably) safely with imperfect knowledge all the time!"
- read `P(cloudy) = 0.0`: no chance (0% chance) of cloudy, definitely will not be cloudy. `P(cloudy) = 1.0` means definitely will be cloudy (100% chance)
- `P(cloudy | measurement)`: reads "best estimate for the probability that it is cloudy, given the `measurement`"
    > Self driving cars take new sensor measurements as often as possible to ensure the data they use to make probabilistic predictions is as "fresh" (and therefore as useful) as possible.
- **conditional probability**: taking advantage from what we know to make better estimate of what we don't, ie:
    - `P(cloudy | measurement)`: use current weather as `measurement` to estimate the chance of being cloudy in next 5 minutes
- **Dependant Event**:  *Two events are dependent if the outcome or occurrence of the first affects the outcome or occurrence of the second so that the probability is changed*, ie. "The outcome of choosing the first card has affected the outcome of choosing the second card"
- sample case of dependant event in medical space:

    ```
    P(POSITIVE | CANCER) = 0.9
    P(NEGATIVE | CANCER) = 0.1
    ```
    → the outcome of the blood test (positive/negative) depends whether the patient has cancer or not. *if the patient has cancer, the probability of the blood test to become positive is 0.9, and negative is 0.1*
- another sample notation: `P(POSITIVE | ¬CANCER) = 0.8` reads *"probability of the test to come up positive when the patient HAS NO cancer is 80%"*
- you can build truth table based on probability values
- given `P(CANCER) = 0.1` and `P(POSITIVE | CANCER) = 0.9`, what's value of `P(CANCER | POSITIVE)` ? 
    - ans (0.09): 
    
        ```
        ‣ P(CANCER | POSITIVE) = P(CANCER) * P(POSITIVE)
        ‣ P(CANCER | POSITIVE) = 0.1 * 0.9
        ‣ P(CANCER | POSITIVE) = 0.09 ✔ 
        ```
    - the notation of above question is this:
        
        ```
        CANCER      TEST    P( )
           Y         P        ?   (ans: 0.09)
           Y         N
           N         P
           N         N
        ```
- propeller drivers air in a particular direction. it can be a ***tractor*** which pulls air downward thru the propeller, or ***pusher***, which push the air upward. quadrocopter, the propellers act as tractor to drive the drone upward
- the more the number of tests, the closer the result to the probability. think of how close 10 coin toasts make to create 50% chance of getting heads compared to 1000 coin toasts. the 1000 toasts will make the 50% chance more probable (consistent)

---

- i took probability course in my uni. but i learnt deeper about probability in this self-driving course.
