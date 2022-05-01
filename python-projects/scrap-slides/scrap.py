import ssl

import requests
import urllib.request
from bs4 import BeautifulSoup

if __name__ == '__main__':
    # url = 'https://www.slideshare.net/Hadoop_Summit/w-235phall1pandey'
    url = 'https://www.slideshare.net/Hadoop_Summit/murhty-saha-june26255pmroom212'

    response = requests.get(url)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        # print(soup)

        slide_container = soup.select("#slide-container")[0]
        divs = slide_container.select('.slide')

        for i, div in enumerate(divs):
            img = div.img
            src = img.attrs.get('src', '')
            print(src)

            urllib.request.urlretrieve(src, f'img/slide_{i+1}.jpg')

    print('end of main')
