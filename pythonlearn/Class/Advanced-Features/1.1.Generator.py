
import time
from collections import deque               # 1.

class Dispatcher(object):                   # 2.
    def __init__(self, tasks):
        self.tasks = deque(tasks)           # 3.

    def next(self):
        return self.tasks.pop()             # 4.

    def run(self):
        while len(self.tasks):              # 5.
            task = self.next()
            try:
                next(task)                  # 6.
            except StopIteration:
                pass                        # 7.
            else:
                self.tasks.appendleft(task) # 8.

def greeting(obj, times):                  # 9.
    for i in range(1, times+1):
        yield                             # 10.
        print("Hello, %s: %d!" % (obj, i))


dispatcher = Dispatcher([
    greeting('work1', 5),
    greeting('work2', 4),
    greeting('work3', 6),
])

dispatcher.run()


# Hello, work3: 1!
# Hello, work2: 1!
# Hello, work1: 1!
# Hello, work3: 2!
# Hello, work2: 2!
# Hello, work1: 2!
# Hello, work3: 3!
# Hello, work2: 3!
# Hello, work1: 3!
# Hello, work3: 4!
# Hello, work2: 4!
# Hello, work1: 4!
# Hello, work3: 5!
# Hello, work1: 5!
# Hello, work3: 6!