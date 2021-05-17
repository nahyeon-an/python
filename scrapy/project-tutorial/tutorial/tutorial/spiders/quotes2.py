import scrapy

class QuotesSpider2(scrapy.Spider):
    name = 'quotes2'

    # start_urls -> start_request method를 자동 실행
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'quotes-{page}.html' # f'string' : 문자열 내부에 외부 변수를 삽입할 수 있는 문자열서식
        with open(filename, 'wb') as f:
            f.write(response.body)
