# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
from pymongo import MongoClient
from scrapy import log
from scrapy.conf import settings
from twisted.enterprise import adbapi
import MySQLdb.cursors
from scrapy import signals
from scrapy.exceptions import DropItem
class LianjiaPipeline(object):
    def __init__(self):
        client=MongoClient(settings['MONGODB_SERVER'],
                           settings['MONGODB_PORT'])

        db=client[settings['MONGODB_DB']]
        self.collection=db[settings['MONGODB_COLLECTION']]
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item
        #self.collection.insert(dict(item))
        #valid=True
        #for data in item:
        '''
            if not data:
                valid=False
                raise DropItem("missing")
        '''
        #if valid:
        #print 'detail of items', dict(item)
        #self.collection.insert(dict(item))
        #print "Update in DB"


class MySQLStoreHouse(object):
    def __init__(self,dbpool):
        self.dbpool=dbpool

    @classmethod
    def from_settings(cls,settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool=adbapi.ConnectionPool('MySQLdb',**dbargs)
        return cls(dbpool)

    def process_item(self,item,spider):
        d=self.dbpool.runInteraction(self._do_upinsert,item,spider)
        d.addErrback(self._handle_error,item,spider)
        d.addBoth(lambda  _:item)
        return d

    def _handle_error(self,failure,item,spider):
        log.err(failure)

    def _do_upinsert(self,conn,item,spider):
        #print 'do upinsert item ', item['building_date']
        conn.execute('''
        insert into house ( name,city_name,location,building_type)
        values ('%s','%s','%s','%s')  
        ''' %(item['name'],item['city_name'],item['location'],item['building_type']))


class MyStoreData(object):
    pass
