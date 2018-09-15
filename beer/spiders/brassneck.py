# -*- coding: utf-8 -*-
import scrapy
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
        page = response.url.split("/")[-2]
        filename = 'brassneck-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

        brewery = Brewery()
        brewery['name'] = 'Brassneck Brewery'
        brewery['address'] = '2148 Main St Vancouver BC'
        brewery['url'] = 'http://brassneck.ca'
        brewery['growlers'] = []
        brewery['tasting_room'] = []

        ontap = Selector(response).xpath('//*[@id="ontap-footer"]/ul/li')
        self.log('Extracted list of beers on tap')
        for beer in ontap:
            item = Beer()
            url = beer.xpath('./a/@href').extract()
            item['url'] = url[0]
            # self.log(url[0])
            # self.log('BEER NAME:')
            beername = beer.xpath('./a/span/text()').extract()
            # self.log(beername[0].strip())
            item['name'] = beername[0].strip()
            # self.log('BEER TYPE:')
            beertype = beer.xpath('./a/ul/li/text()').extract()
            # self.log(beertype[0].strip())
            item['style'] = beertype[0].strip()
            item['abv'] = beertype[1].strip()
            brewery['tasting_room'].append(item)

        growlers = Selector(response).xpath(('//*[@id="fills-footer"]/ul/li'))
        self.log('Extracted list of beers for growler fill:')
        for beer in growlers:
            item = Beer()
            url = beer.xpath('./a/@href').extract()
            item['url'] = url[0]
            # self.log(url[0])
            # self.log('BEER NAME:')
            beername = beer.xpath('./a/span/text()').extract()
            # self.log(beername[0].strip())
            item['name'] = beername[0].strip()
            # self.log('BEER TYPE:')
            beertype = beer.xpath('./a/ul/li/text()').extract()
            # self.log(beertype)
            # self.log(beertype[0].strip())
            item['style'] = beertype[0].strip()
            item['abv'] = beertype[1].strip()
            brewery['growlers'].append(item)

        # print('Brewery Extracted: \n %s' % brewery)
        yield brewery
