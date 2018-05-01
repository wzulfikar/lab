#!/usr/bin/env python

import sys
import wave
import time
import numpy as np

from websocket import create_connection

from wav_visdom import WavVisdom


class wav_ws:
    """wrapper for python websocket"""

    def __init__(self, url: str, dummy: False):
        self.dummy = dummy

        if self.dummy:
            print('wav_ws initiated with dummy mode ON')
            return

        self.ws = create_connection(url)

    def send_binary(self, in_data) -> None:
        if self.dummy:
            return
        self.ws.send_binary(in_data)

    def close(self) -> None:
        if self.dummy:
            print('[DUMMY] wav_ws.close')
            return
        self.ws.close()


def ws_stream_wav(url: str,  # websocket connection
                  wav_file: str,
                  result: dict,
                  dummy: bool,
                  plot: False)-> (int, float):
    print("using websocket to stream wav file:")
    print("- file:", wav_file)
    print("- endpoint:", url)

    if result is not None:
        if 'frames_sent' not in result or 'duration_sent' not in result:
            print('invalid result object: \
                  either frames_sent or duration_sent is not found')
            exit(1)

    plotter = WavVisdom() if plot else None

    ws = wav_ws(url, dummy)

    wf = wave.open(wav_file, 'r')
    nframes = wf.getnframes()

    # frame rate, also referred as sampling rate (or sample rate),
    # is the number of samples of audio carried per second.
    framerate = wf.getframerate()

    sampwidth = wf.getsampwidth()
    channels = wf.getnchannels()

    # duration in seconds
    duration = nframes / float(framerate)

    # frame per ms
    fpms = int(nframes / (duration * 1000))

    print()
    print("wav file info:")
    print("- nframes:", nframes)
    print("- channels:", channels)
    print("- duration:", duration, "seconds")
    print("- frame rate:", framerate)
    print("- sample width:", sampwidth)
    print("- frame per ms:", fpms)

    target_rate = 16000
    if target_rate != framerate:
        print('[ERROR] frame rate (sample rate) does not match target rate: {} != {}'.format(
            framerate, target_rate))
        return

    # https://stackoverflow.com/questions/47865690/how-to-get-number-of-framesor-samples-per-sec-or-ms-in-a-audio-wav-or-mp3
    first_frame = wf.readframes(1)
    sampleRate = np.fromstring(first_frame, np.int16)
    print("- sample rate:", sampleRate)

    print()

    frames_sent = 0

    # send ms worth of frames in each packet
    ms_per_frame = 20
    rate = fpms * ms_per_frame
    print("→ sending {} frames ({}ms) per iteration:".format(rate,
                                                             ms_per_frame))

    # adjust this if you get stuttering voice
    # during playback (ie. via pyaudio)
    stream_wait_ms_adjust = 0.01
    stream_wait_ms = (ms_per_frame / 1000) - stream_wait_ms_adjust
    print('- stream wait (ms):', stream_wait_ms)

    while(frames_sent < nframes):
        if frames_sent + rate > nframes:
            rate = nframes - frames_sent

        waveData = wf.readframes(rate)
        frames_sent += rate

        # send the audio binary and sleep after
        # ms_per_frame to mimic streaming process
        ws.send_binary(waveData)
        time.sleep(stream_wait_ms)

        if plotter is not None:
            plotter.draw(waveData,
                         framerate,
                         frames_sent,
                         nframes)

        progress = int(frames_sent / nframes * 100)
        print('  frame {} of {} ({}%)'.format(
            frames_sent,
            nframes,
            progress),
            end="\r")

        if result is not None:
            result['frames_sent'] = frames_sent
            result['duration_sent'] = frames_sent / fpms / 1000

    # time.sleep(5)
    ws.close()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Waver - stream audio to websocket endpoint")
        print("USAGE : waver.py <endpoint> <wav-file>")
        print("      : waver.py ws://localhost:8000/socket recording1.wav")
        exit()
    result = {'frames_sent': 0, 'duration_sent': 0.}

    try:
        ws_stream_wav(
            sys.argv[1],
            sys.argv[2],
            plot=False,
            dummy=False,
            result=result)

    except KeyboardInterrupt:
        print("\n\nreceived keyboard interrupt")
    except Exception as e:
        print("[ERROR]", e)
    finally:
        print("\n[DONE] length of audio sent: {:.1f} seconds".format(
            result['duration_sent']))

    print()
    print("main exited")
