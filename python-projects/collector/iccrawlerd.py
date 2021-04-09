import threading
import sys
import time
import datetime as dt
from datetime import datetime
# custom
from iccrawler import IncruitCrawler

class CrawlingThread(object):

    def __init__(self, save_path):
        self.save_path = save_path
        self.oldTotal = 3553

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        while True:
            ic_crawler = IncruitCrawler("chromedriver path")

            cnt = 0
            while cnt < 1:
                try:
                    self.newTotal = ic_crawler.get_resume_num()
                    cnt += 1
                except:
                    continue
                finally:
                    ic_crawler.close()

            self.diff = self.newTotal - self.oldTotal

            if self.diff > 0:
                letters = ic_crawler.request_letter(self.diff)
                ic_crawler.close()

                today = datetime.today()
                for i in range(self.diff):
                    filename = "ic-" + str(today.year) + "-" + str(today.month) + "-" + str(today.day) \
                               + "-" + str(today.hour) + "-" + str(today.minute) + "-" + str(self.oldTotal + i + 1) + ".txt"

                    f = open(self.save_path + filename, "wt")
                    f.write(letters[i])
                    f.close()

            elif self.diff == 0:
                ic_crawler.close()
            else:
                print("exception")

            self.oldTotal = self.newTotal

            time.sleep(self.get_interval())

    def get_interval(self):
        tdy = datetime.today()
        # 05:00 AM 에 크롤링 시도
        tmr = datetime(tdy.year, tdy.month, tdy.day, 5, 0)
        if tdy.hour >= 5:
            tmr += dt.timedelta(days=1)

        return (tmr - tdy).total_seconds()


if __name__ == '__main__':
    # usage : nohup python jkcrawlerd.py {naver id} {naver pw} {saving path} {chromedriver path}
    saving = "test/"
    crawler = CrawlingThread(saving)

    while True:
        time.sleep(10)

