import visdom
import numpy as np


class WavVisdom:
    def __init__(self):
        # default opens up to http://localhost:8097
        # make sure visdom server is running:
        # `python -m visdom.server`
        self.v = visdom.Visdom()
        self.canvas = 'wav_visdom'
        assert self.v.check_connection()

        print('visdom is up')

        if not self.v.win_exists(self.canvas):
            self.v.bar(np.zeros(shape=(80, 1)), win=self.canvas)

        self.counter = 0

    def draw(self, waveData, framerate, frames_sent, nframes):
        self.counter += 1

        # every 2 * ms_per_frames
        if self.counter == 3:
            self.counter = 0
            # resample to 2
            signal = np.fromstring(waveData, 'Int16')

            # resize each item
            signal = [x / 200 for x in signal]
            self.v.bar(signal, win=self.canvas)

        # clear plot in last frame
        if frames_sent == nframes:
            self.v.bar(np.zeros(shape=(80, 1)), win=self.canvas)
            return
