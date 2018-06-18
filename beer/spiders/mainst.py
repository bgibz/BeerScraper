import scrapy
from scrapy.selector import Selector

from beer.items import BeerItem


class BrassneckSpider(scrapy.Spider):

    name = 'mainst'
    allowed_domains = ['mainstreetbeer.ca']
    start_urls = ['http://mainstreetbeer.ca/']

    def start_requests(self):
        urls = [
            'http://mainstreetbeer.ca/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'mainstreetbeer-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

        wrapper = Selector(response).xpath("//div[@class='portfolio-wrap ']")[0]
        self.log('Extracted list of beers on tap')
        self.log("ONTAP: ")
        ontap = wrapper.xpath('./div/child::*')
        # self.log('NEXT: %s' % ontap)
        for beer in ontap:
            item = BeerItem()
            url = beer.xpath('.//div[@class="work-info"]/a/@href').extract()
            self.log('BEER: %s' % url[0])
            name = beer.xpath('.//div[@class="vert-center"]/h3/text()').extract()
            self.log('NAME: %s' % name[0])

        growlerWrapper = Selector(response).xpath("//div[@class='portfolio-wrap ']")[0]
        self.log('Extracted list of beers for fills')
        self.log("GROWLERS: ")
        fills = wrapper.xpath('./div/child::*')
        # self.log('NEXT: %s' % ontap)
        for beer in fills:
            item = BeerItem()
            url = beer.xpath('.//div[@class="work-info"]/a/@href').extract()
            self.log('BEER: %s' % url[0])
            name = beer.xpath('.//div[@class="vert-center"]/h3/text()').extract()
            self.log('NAME: %s' % name[0])
