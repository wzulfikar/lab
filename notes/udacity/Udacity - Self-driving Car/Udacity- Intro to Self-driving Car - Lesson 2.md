## Udacity: Intro to Self-driving Car
> Sat, 14 Apr 2018 at 2:00:23 MYT

Preview link: https://classroom.udacity.com/courses/nd113-preview

### Lesson 2: Finding Lane Lines

- in python, make sure to copy arrays (ie. using `numpy.copy()`) instead of just using `=` (ie. `array_a = array_b`) because it's mutable
- ROI: region of interest
- region masking technique:
    - define thresholds
    - extract region of interest
    - mask color and region selection

#### Canny Edge Detection
- canny edge detection is an edge detection algorithm, developed by John F. Canny in 1986
- the canny edge detection has been one of the default edge detectors in image processing
- goal of canny edge detection: detect the boundary of an object in image
- steps to do canny edge detection in a nutshell: 
    1. convert image to grayscale
    2. compute the gradient: at this step, the brightness in each pixel will correspond to the strength of the gradient at that point
    3. find the edges by tracing out the pixels that follow the strongest gradient
- opencv has built-in function to perform canny edge detection: 
    ```
    edges = cv2.Canny(im_gray, low_threshold, high_threshold)
    ```
    - the algorithm will first detect strong edge (strong gradient) pixels above the `high_threshold`
    - reject pixels below the `low_threshold`.
    - pixels with values between the `low_threshold` and `high_threshold` will be included as long as they are connected to strong edges
    - the output edges is a binary image with white pixels tracing out the detected edges and black everywhere else. See the [OpenCV Canny Docs](http://docs.opencv.org/2.4/doc/tutorials/imgproc/imgtrans/canny_detector/canny_detector.html) for more details.

- as far as a ratio of `low_threshold` to `high_threshold`, John Canny himself recommended a low to high ratio of 1:2 or 1:3.
- derivative in image operation:
    - small derivative == small change
    - big derivative == big change
- we expect to find edges where the pixel values are changing *rapidly*
- it's common to include additional Gaussian smoothing before running Canny, which is essentially a way of suppressing noise and spurious gradients by averaging (check out the OpenCV docs for GaussianBlur). `cv2.Canny()` actually applies Gaussian smoothing internally, but we include it here because you can get a different result by applying further smoothing (and it's not a changeable parameter within `cv2.Canny()`!).
- using opencv, a steps to perform canny edge detection would be:
    1. make gray version of our image
    2. apply gassian blue
    3. apply `cv2.Canny()`

#### Hough Transform

- a method to represent lines in parameter space, devised by Paul Hough in 1962
- hough transform: conversion from image space (x vs y) to hough space (m vs b)
- you can use Hough Transform to find lines from canny edges
- a line in image space translates to a point (a dot) in hough space, and vice versa (a point in image space describes a line in Hough space)
- in hough space, there can't be two parallel line; there must be intersection
- "The intersection point at (m0, b0) represents the line y = m0x + b0 in image space and it must be the line that passes through both points!"
- "The four major intersections between curves in Hough space correspond to the four sides of the square."
- you can use `cv2.HoughLinesP()` to find lines at image using hough transform
- python `imageio` library: a library that provides an easy interface to read and write a wide range of image data, including animated images, volumetric data, and scientific formats
- python `moviepy` library: MoviePy is a Python module for video editing, which can be used for basic operations (like cuts, concatenations, title insertions), video compositing (a.k.a. non-linear editing), video processing, or to create advanced effects. It can read and write the most common video formats, including GIF.
