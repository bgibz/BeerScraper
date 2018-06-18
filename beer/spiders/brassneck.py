# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector

from beer.items import BeerItem


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

        ontap = Selector(response).xpath('//*[@id="ontap-footer"]/ul/li')
        self.log('Extracted list of beers on tap')
        for beer in ontap:
            item = BeerItem()
            self.log('URL:')
            url = beer.xpath('./a/@href').extract()
            item['url'] = url[0]
            self.log(url[0])
            self.log('BEER NAME:')
            beername = beer.xpath('./a/span/text()').extract()
            self.log(beername[0].strip())
            item['title'] = beername[0].strip()
            self.log('BEER TYPE:')
            beertype = beer.xpath('./a/ul/li/text()').extract()
            self.log(beertype[0].strip())
            item['style'] = beertype[0].strip()
            item['brewery'] = "Brassneck"

        growlers = Selector(response).xpath(('//*[@id="fills-footer"]/ul/li'))
        self.log('Extracted list of beers for growler fill:')
        for beer in growlers:
            item = BeerItem()
            self.log('URL:')
            url = beer.xpath('./a/@href').extract()
            item['url'] = url[0]
            self.log(url[0])
            self.log('BEER NAME:')
            beername = beer.xpath('./a/span/text()').extract()
            self.log(beername[0].strip())
            item['title'] = beername[0].strip()
            self.log('BEER TYPE:')
            beertype = beer.xpath('./a/ul/li/text()').extract()
            self.log(beertype[0].strip())
            item['style'] = beertype[0].strip()
            item['brewery'] = "Brassneck"
