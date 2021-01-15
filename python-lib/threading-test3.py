"""
thread를 여러개 만들 때
반복문을 이용하여 join
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

threads = []
for i in range(3):
    thread = Worker(i)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

print("main thread posts job")
print("main thread ends !")