# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs

class ZhihuPipeline(object):
    def process_item(self, item, spider):
        return item



import json

class JsonWriterPipeline(object):

    def __init__(self):
        self.file = codecs.open('items.json', 'w', encoding="utf-8")

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item


import pymongo

from scrapy.conf import settings
from scrapy.exceptions import DropItem

class MongoDBPipeline(object):

    collection_name = settings['MONGO_COLLECTION']

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'circle')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.collection_name]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        matching_item = self.collection.find_one({
            'atoken': item['atoken']
        })
        if matching_item is not None:
            raise DropItem("Duplicate item found: %s" % item['atoken'])
        else:
            self.collection.insert(dict(item))
        return item