import cv2
from datetime import datetime


class RecorderPipeline:
    def __init__(self,
                 pipeline_register,
                 video_capture,
                 storagepath: str,
                 start: bool):
        self.p_reg = pipeline_register
        self._set_args(video_capture, storagepath, start)

    def _set_args(self, video_capture, storagepath: str, start: bool):
        self._writer = None
        self.isrecording = start
        self.storagepath = storagepath
        self.framewidth = video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.frameheight = video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.fps = int(video_capture.get(cv2.CAP_PROP_FPS))

        if self.isrecording:
            self.start_recording(self.fps)

    def closer(self):
        self.stop_recording()

    def start_recording(self, fps: int = None):
        if fps is None:
            fps = self.fps

        print("[RECORDING] recording video at", fps, "fps")
        now = datetime.now()
        self._writer = cv2.VideoWriter(
            '{}/{}.avi'.format(
                self.storagepath,
                now.strftime('%Y-%m-%d_%H%M%S')),
            cv2.VideoWriter_fourcc(*"X264"),
            fps,
            (int(self.framewidth), int(self.frameheight)))

    def stop_recording(self):
        if self._writer is None:
            return

        self._writer.release()

    def process(self, frame):
        if self.isrecording:
            self._writer.write(frame)
