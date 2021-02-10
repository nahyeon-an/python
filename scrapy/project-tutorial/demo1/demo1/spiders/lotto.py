import scrapy


class LottoSpider(scrapy.Spider):
    name = 'lotto'
    allowed_domains = ['dhlottery.co.kr']
    start_urls = ['http://dhlottery.co.kr/gameResult.do?method=byWin']

    def parse(self, response):
        numbers = response.css('div.nums span::text').getall()
        rnd = response.css('div.win_result strong::text').get()
        rnd = rnd[:-1]

        result = {'rnd': rnd}
        for idx, n in enumerate(numbers[:-1], 1):
            result['no{}'.format(idx)] = n

        result['bno'] = numbers[-1]

        yield result
