import scrapy
from scrapy.selector import Selector

from beer.items import Brewery
from beer.items import Beer


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
        brewery = Brewery()
        brewery['name'] = 'Main Street Brewing'
        brewery['address'] = '261 East Seventh Avenue, Vancouver, BC'
        brewery['url'] = 'http://mainstreetbeer.ca/'
        brewery['growlers'] = []
        brewery['tasting_room'] = []

        wrapper = Selector(response).xpath("//div[@class='portfolio-wrap ']")[0]
        ontap = wrapper.xpath('./div/child::*')

        for beer in ontap:
            item = Beer()
            url = beer.xpath('.//div[@class="work-info"]/a/@href').extract()
            item['url'] = url[0]
            name = beer.xpath('.//div[@class="vert-center"]/h3/text()').extract()
            item['name'] = name[0]
            style = name[0].split()
            item['style'] = style[-1].strip()
            brewery['tasting_room'].append(item)

        growlerWrapper = Selector(response).xpath("//div[@class='portfolio-wrap ']")[0]
        fills = wrapper.xpath('./div/child::*')
        for beer in fills:
            item = Beer()
            url = beer.xpath('.//div[@class="work-info"]/a/@href').extract()
            item['url'] = url[0]
            name = beer.xpath('.//div[@class="vert-center"]/h3/text()').extract()
            style = name[0].split()
            item['style'] = style[-1].strip()
            brewery['growlers'].append(item)

        yield brewery
