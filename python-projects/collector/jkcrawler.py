from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pyperclip
import requests

class JobKoreaCrawler:

    def __init__(self, naver_id, naver_pw, os_option, chromedriver):
        self.id = naver_id
        self.pw = naver_pw
        self.os_option = os_option
        self.chromedriver = chromedriver

        self.options = webdriver.ChromeOptions()
        self.options.add_argument('headless')
        self.options.add_argument('disable-gpu')
        self.options.add_argument('lang=ko_KR')
        self.driver = webdriver.Chrome(self.chromedriver, options=self.options)

        self.req_url = "https://www.jobkorea.co.kr"

    def start(self):
        """
        합격자소서 리스트가 존재하는 페이지까지 진입
        """
        self.driver.get("https://www.jobkorea.co.kr/")
        time.sleep(1)

        self.driver.find_element_by_xpath("//button[@title='네이버 로그인']").click()
        time.sleep(1)

        self.driver.switch_to.window(self.driver.window_handles[-1])
        time.sleep(1)

        id_element = self.driver.find_element_by_id('id')
        id_element.click()
        time.sleep(1)
        pyperclip.copy(self.id)
        if self.os_option == 'm':
            id_element.send_keys(Keys.COMMAND, 'v')
        elif self.os_option == 'w':
            id_element.send_keys(Keys.CONTROL, 'v')
        time.sleep(1)

        pw_element = self.driver.find_element_by_id('pw')
        pw_element.click()
        time.sleep(1)
        pyperclip.copy(self.pw)
        if self.os_option == 'm':
            pw_element.send_keys(Keys.COMMAND, 'v')
        elif self.os_option == 'w':
            pw_element.send_keys(Keys.CONTROL, 'v')
        time.sleep(1)

        self.driver.find_element_by_xpath("//input[@id='log.login']").click()
        time.sleep(1)
        self.driver.close()

        self.driver.switch_to.window(self.driver.window_handles[0])

        self.driver.find_element_by_xpath("//div[@class='jkNavArea']/ul[1]/li[2]/a").click()
        self.driver.find_element_by_xpath("//div[@class='starSideNav']/div[4]/ul/li[1]/a").click()
        time.sleep(1)

        self.driver.find_element_by_xpath("//div[contains(@class, 'firstPopUp')]/div/button").click()
        time.sleep(1)

    def get_resume_num(self):
        """
        합격자소서의 총 개수를 반환 (integer)
        """
        import re

        self.start()

        self.first_page = self.driver.page_source
        soup = BeautifulSoup(self.first_page, 'html.parser')

        todayTotal = soup.select("#container > div.stContainer > div:nth-child(4) > h4 > span:nth-child(2)")[0]
        nums = "".join(re.findall("\d+", todayTotal.contents[0]))
        self.todayTotal = int(nums)

        return self.todayTotal

    def request_letter(self, cnt):
        """
        cnt 개수 만큼의 자소서를 위에서부터 크롤링하여 텍스트 내용을 리스트로 반환
        """
        if self.first_page is None:
            self.first_page = self.driver.page_source

        soup = BeautifulSoup(self.first_page, 'html.parser')

        addrs = soup.select("div > .ctTarget")[0].select("ul.selfLists > li > a")
        if len(addrs) < cnt:
            print("page 넘김 필요 -> 버튼 눌러야 함")

        ret = []
        for i in range(cnt-1, -1, -1):
            req = requests.get(self.req_url + addrs[i].attrs['href'])
            text = req.text
            ret.append(text)

        return ret

    def close(self):
        self.driver.quit()


if __name__ == '__main__':
    jk_crawler = JobKoreaCrawler("naver id", "naver pw", "m or w", "chromedriver path")

    print("start")

    n = jk_crawler.get_resume_num()

    print("nums : {}".format(n))

    letters = jk_crawler.request_letter(2)

    print(len(letters))

    jk_crawler.close()
