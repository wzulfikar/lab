import threading
import time


class WithThread(threading.Thread):
    """pass a function and its payload to run in thread"""

    def __init__(self, fn, *payload):
        threading.Thread.__init__(self)
        self.locals = locals()

    def run(self):
        self.locals['fn'](*self.locals['payload'])


def command1(delay, name):
    print('command1:', name, 'sleeping for', delay)
    time.sleep(delay)
    print('[DONE]', name)


def command2(name):
    print('command2:', 'hello', name)
    print('[DONE]', name)


if __name__ == "__main__":
    threads = {}
    for x in range(1, 5):
        threads[x] = WithThread(command1, 2, 'thread #{}'.format(x))
        threads[x].start()

    for x in range(6, 10):
        threads[x] = WithThread(command2, 'thread #{}'.format(x))
        threads[x].start()

    # tell python to wait till all threads to finish.
    # comment below code and `print("done")` will be
    # executed before the threads finished.
    for i, t in threads.items():
        t.join()

    print("main exited")
