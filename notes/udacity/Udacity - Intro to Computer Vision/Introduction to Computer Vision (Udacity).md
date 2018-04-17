## Introduction to Computer Vision (Udacity)
> George University
> https://classroom.udacity.com/courses/ud810

### Lesson 1: Introduction

1. CV: computer vision
- CP: computational photography
- illusion of power: "I called Megan and she comes."
    
    > but megan has the real power, which is video editing
- Prof. Aron Bobick (funny :v)
- goal of CV: write computer program that can *interpret* images
- how to make computer processes video and recognize actions?
- IEEE Journal: **The Faces of Engagement: Automatic Recognition of Student Engagementfrom Facial Expressions** → https://ieeexplore.ieee.org/document/6786307/
- cgi: industrial light and magic (ILM): ilm.com
- what's the deal with computer vision:
    - object recognition
    - OCR
    - face recognition
    - special effects and 3D modelling
    - smart cars
    - sports
    - vision based interaction (xbox kinect depth image, etc)
    - security (surveilance, etc)
    - medical imaging (image-guided surgery, etc)
- ***vision IS NOT image processing***
- your brain tell you what you see, hence it can creates *illusion*
- the triangle in computer vision:
    - computational models (math)
    - algorithm
    - real images
- [octave](https://www.gnu.org/software/octave/): open-source equivalent for matlab
- install octave macos: `brew install octave`
- read more: https://wiki.octave.org/Octave_for_macOS

### Lesson 2: Images as Functions
- an image can be thought of:
    - a function of `I(x, y)`: give the intensity or value at position (x, y)
    - a 2D array of numbers ranging from some minimum to some maximum (0 to 255)
- above function `I(x, y)` represents single channel image (monochrome, black and white, etc). a color image will have a stacked function (vector-valued) like this:

    ```
    f(x, y) = | r(x, u) | # r for red
              | g(x, u) | # g for green
              | b(x, u) | # b for blue
    ```
- an image is mapping of `f(x,y)` to intensity, which looks like this:

    ```
    x = (10, 210)
    y = (15, 165)
    intensity = (0, 10)
    image = f(x, y) + intensity
    ```
- rgb (red, green, blue) = 3 channels/planes
- "A 3-channel color image is a **mapping** from a 2-dimensional space of locations to a 3-dimensional space of color intensity values."
- 3 channels color image can be thought as this function:

    ```
    f: R * R → R * R * R
      [x] [y] [intensity]
    ```
- `sample`: the 2D space on a regular grid
- `quantize`: each sample (round to nearest integer)
- TIL: `pixel` stands for picture element
- based on above knowledges on image (image as function, its mapping to intensity, etc), we can say that **a digital image is a representation of a matrix of integer values**
- in digital images, the height of a picture is equivalent to its rows, its width is equivalent to columns, and its area (h*w) is equivalent to pixels
- in a colored digital image, each pixel contains multiple different colors (or channel/plane), ie. red, green, blue in each pixel means a 3-channel digital image
- **MATLAB INDEXING STARTS AT 1!!** and so does `octave`
- draw line on image using octave;

    ```
    # load image
    im = imread('images/bali.jpg')
    
    # display the image
    imshow(im)
    
    # draw the line
    line([1 512],[256 256], 'color', 'r')
    ```
- quantizing image: 
    - to quantize an image, convert each number in the matrix and round down (floor function)
- use `size()` to get size of an image:

    ```
    # using octave
    > size(img)
    ans =

    768   1024      3
    ```
- 8 "byte" = indicates the bit depth 
- addition of image is element by element operation. hence, the size of images must match.
- `uint8` = 0 to 255
- be mindful of data type of the image you're using when doing arithmetic operation

---
review:

- overall fun learning process, fun instructor and fun way of communicatin the materials
- bit-sized, succinct materials
- prbbly my first enjoyable and learnable online lecture video on a considerably more serious topic
