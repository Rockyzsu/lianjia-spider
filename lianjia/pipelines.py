# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from lianjia import settings
from scrapy.exceptions import DropItem
class LianjiaPipeline(object):
    def __init__(self):
        client=MongoClient('localhost',
            27017)

        db=client['test']
        self.collection=db['houseinfo']
    def process_item(self, item, spider):
        valid=True
        for data in item:
            if not data:
                valid=False
                raise DropItem("missing")
        if valid:
            self.collection.insert(dict(item))
            print "Update in DB"
        return item
