"""
thread 기본 및 daemon 설정
"""
import threading
import time

class Worker(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        print("sub thread starts ", threading.currentThread().getName())
        time.sleep(3)
        print("sub thread ends ", threading.currentThread().getName())

print("main thread starts !")
for i in range(5):
    name = "thread {}".format(i)
    t = Worker(name)
    t.daemon = True
    t.start()

print("main thread ends !")