import scrapy

class QuotesSpider4(scrapy.Spider):
    name = 'quotes4'

    # start_urls -> start_request method를 자동 실행
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        quotes = response.css('div.quote')
        for quote in quotes:
            yield {
                'text' : quote.css('span.text::text').get(),
                'author' : quote.css('small.author::text').get(),
                'tags' : quote.css('div.tags a.tag::text').getall()
            }
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(url=next_page, callback=self.parse)
