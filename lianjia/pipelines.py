# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from scrapy.conf import settings
from scrapy.exceptions import DropItem
class LianjiaPipeline(object):
    def __init__(self):
        client=MongoClient(settings['MONGODB_SERVER'],
                           settings['MONGODB_PORT'])

        db=client[settings['MONGODB_DB']]
        self.collection=db[settings['MONGODB_COLLECTION']]
    def process_item(self, item, spider):
        valid=True
        for data in item:
            if not data:
                valid=False
                raise DropItem("missing")
        if valid:
            print 'detail of items', dict(item)
            self.collection.insert(dict(item))
            print "Update in DB"
        return item
