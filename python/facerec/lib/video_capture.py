import cv2


class VideoCapture:
    def __init__(self, source: str):
        """wrapper for cv2.VideoCapture"""
        
        if source.isdigit():
            self.capture, self.info = cv2.VideoCapture(
                int(0)), "<device {}>".format(source)
        else:
            self.capture, self.info = cv2.VideoCapture(
                source), "<{}>".format(source)
