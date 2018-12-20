# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field;


class Brewery(Item):
    last_updated = Field()
    name = Field()
    address = Field()
    growlers = Field()
    tasting_room = Field()
    url = Field()


class Beer(Item):
    name = Field()
    style = Field()
    abv = Field()
    url = Field()


class BeerItem(Item):
    name = Field()
    style = Field()
    abv = Field()
    url = Field()
