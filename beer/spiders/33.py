# -*- coding: utf-8 -*-
import scrapy
import datetime
from scrapy.selector import Selector

from beer.items import Beer
from beer.items import Brewery


class ThirtyThreeAcresSpider(scrapy.Spider):

    name = '33acres'
    allowed_domains = ['http://33acresbrewing.com']
    start_urls = ['http://http://33acresbrewing.com/our-beers/']

    def start_requests(self):
        urls = [
            'http://33acresbrewing.com/our-beers/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        brewery = Brewery()
        brewery['last_updated'] = datetime.datetime.utcnow()
        brewery['name'] = '33 Acres Brewing'
        brewery['address'] = '15 W 8th Ave, Vancouver BC'
        brewery['url'] = 'http://33acresbrewing.com'
        brewery['growlers'] = []
        brewery['tasting_room'] = []

        ontap = Selector(response).xpath('//div[contains(@class, "beer-info")]')
        print('Extracted list of beers on tap: %s' % ontap)
        for beer in ontap:
            item = Beer()
            # url = beer.xpath('./a/@href').extract()
            item['url'] = 'http://http://33acresbrewing.com/our-beers/'
            beername = beer.xpath('./h1/text()').extract()
            if beername == []:
                beername = beer.xpath('./a/h1/text()').extract()
            # print("Beer: %s" % beername)
            item['name'] = beername[0].strip()

            info = beer.xpath('./h4/text()').extract()
            beertype = info[0].split(': ')[1]
            # print("Type: %s" % beertype)
            item['style'] = beertype.strip()

            abv = info[2].split(': ')[1]
            abv = abv.split(' ')[0]
            # print("ABV: %s" % abv)
            item['abv'] = abv.strip()

            methods = beer.xpath('./h2/text()').extract()

            if "Glasses" in methods[0]:
                brewery['tasting_room'].append(item)
            if "Growler" in methods[0]:
                brewery['growlers'].append(item)

        yield brewery
