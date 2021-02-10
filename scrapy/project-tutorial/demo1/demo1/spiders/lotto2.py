import scrapy
from scrapy import FormRequest


class LottoSpider2(scrapy.Spider):
    name = 'lotto2'
    allowed_domains = ['dhlottery.co.kr']
    start_urls = ['http://dhlottery.co.kr/gameResult.do?method=byWin']

    def parse(self, response):

        rnd = self.rnd # 실행 시 인자로 전달 받는 값 -a rnd=940

        if response.status == 200:
            yield FormRequest.from_response(response=response,
                                      method='POST',
                                      formdata={'drwNo': str(rnd), 'dwrNoList': str(rnd)},
                                      callback=self.parse_numbers)

    def parse_numbers(self, response):
        numbers = response.css('div.nums span::text').getall()
        rnd = response.css('div.win_result strong::text').get()
        rnd = rnd[:-1]

        result = {'rnd': rnd}
        for idx, n in enumerate(numbers[:-1], 1):
            result['no{}'.format(idx)] = n

        result['bno'] = numbers[-1]

        yield result
