import scrapy
from scrapy.selector import Selector

from beer.items import BeerItem


class BrassneckSpider(scrapy.Spider):

    name = 'bomber'
    allowed_domains = ['bomberbrewing.com']
    start_urls = ['http://bomberbrewing.com']

    def start_requests(self):
        urls = [
            'http://bomberbrewing.com/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'bomberbrewing-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

        growlers = Selector(response).xpath('//*[@id="menu-container"]/div/div[3]/div/div[2]/div[2]/div[1]')
        self.log(growlers)
        # JS required. Abandon for now
