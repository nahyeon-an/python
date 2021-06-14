from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request
import time
import logging, traceback

chromedriver = '/Users/nahyeonan/Downloads/chromedriver'
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('disable-gpu')
options.add_argument('lang=ko_KR')
driver = webdriver.Chrome(chromedriver, options=options)
driver.get('https://www.google.co.kr/imghp?hl=ko')
time.sleep(1)
driver.find_element_by_name('q').send_keys('원피스 루피 기어포스 바운드맨')
time.sleep(1)
driver.find_element_by_xpath('//*[@id="sbtc"]/button').click()
time.sleep(1)
page = driver.page_source

soup = BeautifulSoup(page, 'html.parser')
content = soup.select("#islrg > div")[0]

print(len(content))
img_logger = logging.getLogger("img_logger")
img_logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('img_crawling.log')
img_logger.addHandler(file_handler)

cnt = 1
for c in content:
    try:
        img_tag = c.select("img")[0]
        if 'src' in img_tag.attrs:
            src = img_tag.attrs['src']
        # elif 'data-src' in img_tag.attrs:
        #     src = img_tag.attrs['data-src']
        urllib.request.urlretrieve(src, "img/boundman_img_{0}.jpg".format(cnt))
        cnt += 1
    except Exception as e:
        img_logger.exception(e)
        continue

driver.quit()