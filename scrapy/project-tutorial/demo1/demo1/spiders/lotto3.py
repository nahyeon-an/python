import scrapy
from scrapy import FormRequest


class LottoSpider3(scrapy.Spider):
    name = 'lotto3'
    allowed_domains = ['dhlottery.co.kr']

    def start_requests(self):

        # self.start
        # self.end
        self.rnd = int(self.start)

        yield FormRequest(url='https://dhlottery.co.kr/gameResult.do?method=byWin',
                          method='POST',
                          formdata={'drwNo': str(self.rnd), 'dwrNoList': str(self.rnd)},
                          callback=self.parse)

    def parse(self, response):
        numbers = response.css('div.nums span::text').getall()
        rnd = response.css('div.win_result strong::text').get()
        rnd = rnd[:-1]

        result = {'rnd': rnd}
        for idx, n in enumerate(numbers[:-1], 1):
            result['no{}'.format(idx)] = n

        result['bno'] = numbers[-1]

        yield result

        if self.rnd < int(self.end):
            self.rnd += 1

            yield FormRequest(url='https://dhlottery.co.kr/gameResult.do?method=byWin',
                              method='POST',
                              formdata={'drwNo': str(self.rnd), 'dwrNoList': str(self.rnd)},
                              callback=self.parse)
