# -*- coding: utf-8 -*-
import scrapy
import datetime
from scrapy.selector import Selector

from beer.items import Beer
from beer.items import Brewery

class BrassneckSpider(scrapy.Spider):

    name = 'brassneck'
    allowed_domains = ['brassneck.ca']
    start_urls = ['http://brassneck.ca']

    def start_requests(self):
        urls = [
            'http://brassneck.ca/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        brewery = Brewery()
        brewery['last_updated'] = datetime.datetimee.utcnow()
        brewery['name'] = 'Brassneck Brewery'
        brewery['address'] = '2148 Main St, Vancouver BC'
        brewery['url'] = 'http://brassneck.ca'
        brewery['growlers'] = []
        brewery['tasting_room'] = []

        ontap = Selector(response).xpath('//*[@id="ontap-footer"]/ul/li')
        self.log('Extracted list of beers on tap')
        for beer in ontap:
            item = Beer()
            url = beer.xpath('./a/@href').extract()
            item['url'] = url[0]
            beername = beer.xpath('./a/span/text()').extract()
            item['name'] = beername[0].strip()
            beertype = beer.xpath('./a/ul/li/text()').extract()
            item['style'] = beertype[0].strip()
            item['abv'] = beertype[1].strip()
            brewery['tasting_room'].append(item)

        growlers = Selector(response).xpath(('//*[@id="fills-footer"]/ul/li'))
        self.log('Extracted list of beers for growler fill:')
        for beer in growlers:
            item = Beer()
            url = beer.xpath('./a/@href').extract()
            item['url'] = url[0]
            beername = beer.xpath('./a/span/text()').extract()
            item['name'] = beername[0].strip()
            beertype = beer.xpath('./a/ul/li/text()').extract()
            item['style'] = beertype[0].strip()
            item['abv'] = beertype[1].strip()
            brewery['growlers'].append(item)

        yield brewery
