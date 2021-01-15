"""
thread join()
"""
import threading
import time

class Worker(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        print("sub thread starts ", threading.currentThread().getName())
        time.sleep(5)
        print("sub thread ends ", threading.currentThread().getName())

print("main thread starts !")

t1 = Worker("1")
t1.start()

t2 = Worker("2")
t2.start()

t1.join()
t2.join()

print("main thread posts job")
print("main thread ends !")