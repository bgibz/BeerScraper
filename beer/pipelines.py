# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo


class BreweryPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        print('init pipeline')
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.collection_name = 'breweries'

    @classmethod
    def from_crawler(cls, crawler):
        # pull in information from settings.py
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        # opening db connection
        print('Open Spider!')
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        # clean up when spider is closed
        self.client.close()

    def process_item(self, item, spider):
        # how to handle each post
        collection = self.db[self.collection_name]
        query = {'name': item['name']}
        brewery = collection.find(query)
        if brewery is None:
            # add brewery
            self.db[self.collection_name].insert(dict(item))
        else:
            # delete existing item, replace with scraped item
            collection.delete_one(query)
            collection.insert(dict(item))
        return item
