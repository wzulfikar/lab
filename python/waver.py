#!/usr/bin/env python

import sys
import wave
import time
import numpy as np

from websocket import create_connection


def ws_stream_wav(url: str,
                  wav_file: str,
                  result: dict,
                  delay: float = 0.)-> (int, float):
    print("using websocket to stream wav file:")
    print("- file:", wav_file)
    print("- endpoint:", url)

    if result is not None:
        if 'frames_sent' not in result or 'duration_sent' not in result:
            print('invalid result object: \
                  either frames_sent or duration_sent is not found')
            exit(1)

    ws = create_connection(url)

    wf = wave.open(wav_file, 'r')
    nframes = wf.getnframes()
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

    # https://stackoverflow.com/questions/47865690/how-to-get-number-of-framesor-samples-per-sec-or-ms-in-a-audio-wav-or-mp3
    first_frame = wf.readframes(1)
    sampleRate = np.fromstring(first_frame, np.int16)
    print("- sample rate:", sampleRate)

    print()

    frames_sent = 0

    # send n of frames worth 20ms of audio
    rate = fpms * 20
    print("→ sending {} frames per iteration;".format(rate))
    while(frames_sent < nframes):
        if frames_sent + rate > nframes:
            rate = nframes - frames_sent

        waveData = wf.readframes(rate)
        frames_sent += rate
        ws.send_binary(waveData)

        progress = int(frames_sent / nframes * 100)
        print('  frame {} of {} ({}%)'.format(
            frames_sent,
            nframes,
            progress),
            end="\r")

        if result is not None:
            result['frames_sent'] = frames_sent
            result['duration_sent'] = frames_sent / fpms / 1000

        if delay > 0:
            time.sleep(delay)

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
            result=result,
            delay=0.)

    except KeyboardInterrupt:
        print("\n\nreceived keyboard interrupt")
    except Exception as e:
        print("[ERROR]", e)
    finally:
        print("\n[DONE] length of audio sent: {:.1f} seconds".format(
            result['duration_sent']))

    print()
    print("main exited")
