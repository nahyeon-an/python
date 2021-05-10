from bs4 import BeautifulSoup
from selenium import webdriver
import time
import requests

class IncruitCrawler:

    def __init__(self, chromedriver):
        self.id = ""
        self.pw = ""
        self.chromedriver = chromedriver

        self.options = webdriver.ChromeOptions()
        self.options.add_argument('headless')
        self.options.add_argument('disable-gpu')
        self.options.add_argument('lang=ko_KR')
        self.options.add_argument("--kiosk")
        self.driver = webdriver.Chrome(self.chromedriver, options=self.options)

        self.req_url = "https://people.incruit.com/resumeguide"

    def start(self):
        self.driver.get("https://people.incruit.com")
        time.sleep(2)

        self.driver.get("https://edit.incruit.com/login/login.asp?gotoURL=https%3A%2F%2Fpeople%2Eincruit%2Ecom%2F")
        # self.driver.find_element_by_xpath('//li[@id="gnb_login"]/button').click()  # browser를 열지 않을 때 동작 안 함 (바로 서브 로그인 페이지로 이동)
        time.sleep(1)
        self.driver.find_element_by_name('txtUserID').send_keys(self.id)
        self.driver.find_element_by_name('txtPassword').send_keys(self.pw)
        time.sleep(1)

        self.driver.find_element_by_xpath('//*[@id="g_form_login_box"]/fieldset/div/button').click()
        time.sleep(1)

        self.driver.find_element_by_xpath('//*[@id="ResumeMainInfoLayer"]/div[1]/button').click()
        time.sleep(1)

        self.driver.find_element_by_xpath('//*[@id="incruit_contents"]/div/div[5]/div[1]/div[1]/h4/a').click()

        self.driver.switch_to.window(self.driver.window_handles[-1])

    def get_resume_num(self):
        """
        합격자소서의 총 개수를 반환 (integer)
        """
        import re

        self.start()

        self.first_page = self.driver.page_source
        soup = BeautifulSoup(self.first_page, 'html.parser')

        todayTotal = soup.select("#incruit_contents > div > div.bbsHeader > p.total > span > em")[0]
        nums = "".join(re.findall("\d+", todayTotal.contents[0]))
        self.todayTotal = int(nums)

        return self.todayTotal

    def request_letter(self, cnt):
        if self.first_page is None:
            self.first_page = self.driver.page_source

        soup = BeautifulSoup(self.first_page, 'html.parser')

        ret = []
        for i in range(cnt, 0, -1):
            link = soup.select("#incruit_contents > div > div.bbsWrap > table > tbody > tr:nth-of-type(" + str(i) \
                                + ") > td:nth-of-type(2) > a")
            req = requests.get(self.req_url + link[0].attrs['href'][1:])
            text = req.text
            ret.append(text)

        return ret

    def close(self):
        self.driver.quit()

if __name__ == '__main__':
    path = "/Users/nahyeonan/Downloads/chromedriver"
    ic_crawler = IncruitCrawler(path)

    cnt = 0
    while cnt < 1:
        try:
            num = ic_crawler.get_resume_num()
            print(num)
            ret = ic_crawler.request_letter(2)
            print(len(ret))
            cnt += 1
        except:
            print()
            continue
        finally:
            ic_crawler.close()
