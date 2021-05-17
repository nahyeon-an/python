from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request
import time

chromedriver = '/Users/nahyeonan/Downloads/chromedriver'
driver = webdriver.Chrome(chromedriver)
driver.get('https://www.google.co.kr/imghp?hl=ko')
time.sleep(1)
driver.find_element_by_name('q').send_keys('원피스 루피 어린시절')
time.sleep(1)
driver.find_element_by_xpath('//*[@id="sbtc"]/button').click()
time.sleep(1)
page = driver.page_source

soup = BeautifulSoup(page, 'html.parser')
content = soup.select("#islrg > div")[0]

print(len(content))  # 46
cnt = 1
for c in content:
    try:
        img_tag = c.select("img")[0]
        if 'src' in img_tag.attrs:
            src = img_tag.attrs['src']
        elif 'data-src' in img_tag.attrs:
            src = img_tag.attrs['data-src']
        urllib.request.urlretrieve(src, "test/img_{0}.jpg".format(cnt))
        cnt += 1
    except:
        print(img_tag)
        continue

driver.quit()