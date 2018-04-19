from concurrent.futures import ThreadPoolExecutor
import time


class Task:
    def __init__(self, name: str):
        self.name = name
        self.counter = 0

    def run(self):
        time.sleep(1)
        self.counter += 1
        print('[TASK {}] counter: {}'.format(self.name, self.counter))


task1 = Task('1')
task2 = Task('2')
task3 = Task('3')

pool1 = ThreadPoolExecutor(max_workers=1)
pool2 = ThreadPoolExecutor(max_workers=1)
pool3 = ThreadPoolExecutor(max_workers=1)


for i in range(5):
    pool1.submit(task1.run)
    pool1.submit(task2.run)
    pool1.submit(task3.run)

print('[DONE] program reached end of line')
