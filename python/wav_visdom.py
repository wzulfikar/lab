import visdom
import numpy as np
from concurrent.futures import ThreadPoolExecutor


class WavVisdom:
    def __init__(self):
        # default opens up to http://localhost:8097
        # make sure visdom server is running:
        # `python -m visdom.server`
        self.v = visdom.Visdom()
        self.canvas = 'wav_visdom'
        self.thread_pool = ThreadPoolExecutor(max_workers=1)

        print('checking visdom.server..')
        print('make sure you have it running (ie. `pip -m visdom.server`)')
        assert self.v.check_connection()

        print('visdom is up')

        if not self.v.win_exists(self.canvas):
            self.v.bar(np.zeros(shape=(80, 1)), win=self.canvas)

        self.counter = 0

    def draw(self, waveData, framerate, frames_sent, nframes):
        self.thread_pool.submit(
            self._draw, waveData, framerate, frames_sent, nframes)

    def _draw(self, waveData, framerate, frames_sent, nframes):
        # resample to 2
        signal = np.fromstring(waveData, 'Int16')[::2]

        # resize each item
        signal = [x / 200 for x in signal]
        self.v.bar(signal, win=self.canvas)

        # clear plot in last frame
        if frames_sent == nframes:
            self.v.bar(np.zeros(shape=(80, 1)), win=self.canvas)
            return
