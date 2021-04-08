import threading
import time
from datetime import datetime


class ThreadingExample(object):
    
    def __init__(self, interval=10):
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                        
        thread.start()                                

    def run(self):
        while True:
            print("start of daemon")
            today = datetime.today()
            filename = "test/" + str(today.hour) + "-" + str(today.minute) + "-" + str(today.second) + ".txt"
            f = open(filename, "wt")
            f.write("writing in background")
            f.close()
            print("end of daemon")

            time.sleep(self.interval)

if __name__ == '__main__':
    example = ThreadingExample()
    while True:
        print("start to sleep")
        time.sleep(20)
        print("end of sleep")