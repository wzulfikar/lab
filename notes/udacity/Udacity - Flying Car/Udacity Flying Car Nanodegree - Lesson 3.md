### Lesson 3: Backyard Flyer
1. flight computer: a higher level program that control where the vehicle should go, etc
2. autopilot: a lower level program, ie. to control thrusts, etc
3. a drone programmer job is likely to deal with writing codes for the flight computer
4. `ipython`: python interactive shell with added features; qt-based, web-based notebook, gui, etc.
5. the simulator will start using port `5760` when the option is selected (Backyard Flyer, Motion Planning, or Controls). the port will be active as long as a session is activated, regardless of the control mode (manual/guided)
6. when running the drone code from python, make sure the simulator mode is set to "GUIDED" (not "MANUAL")
7. running `python` inside conda env will automatically use the python binary from conda
8. you can run from any folder and the dependencies will still be available for given conda environment as long as the packages were installed in the same environment
9. **EDP**: event driven programming; a dominant paradigm used in graphical user interface.
10. an asterisk in jupyter notebook (`[*]`) indicates that the current cell is (still) executing code. this can be used to determine if a cell contains a long-blocking code, etc.
11. a good example for event driven programming: a chatbot program; because in chatbot, programmer can't really know what the user will ask the chatbot. hence, instead of creating a sequential program, an event-driven program paradigm should be used.
12. when doing event driven programming, think above "state variable"

> understanding python asterisk (`*`): https://medium.com/understand-the-python/understanding-the-asterisk-of-python-8b9daaa4a558

---

- relationship between numpy, scipy, pandas & scikit-learn: https://www.quora.com/What-is-the-relationship-among-NumPy-SciPy-Pandas-and-Scikit-learn-and-when-should-I-use-each-one-of-them
