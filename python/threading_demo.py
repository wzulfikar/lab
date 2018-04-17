import threading
import time


class myThread (threading.Thread):
    def __init__(self, threadID, delay):
        threading.Thread.__init__(self)
        self.threadID = threadID
        print("thread #{} created".format(self.threadID))
        self.delay = delay

    def run(self):
        print("Starting", self.threadID)
        print_time('time from thread {}'.format(self.threadID), self.delay)
        print("Exiting thread", self.threadID)


def print_time(threadName, delay):
    print("sleeping for", delay, "seconds")
    time.sleep(delay)
    print("%s: %s" % (threadName, time.ctime(time.time())))


# Create new threads
t1 = myThread(1, 1)
t2 = myThread(2, 2)
# t3 = myThread(2, 2)

# Start new Threads
t1.start()
t2.start()
t1.join()
t2.join()
print("Exiting Main Thread")
