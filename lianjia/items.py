# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
#from scrapy.item import ,Field

class LianjiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name=scrapy.Field()
    city_name = scrapy.Field()
    price = scrapy.Field()
    location=scrapy.Field()
    building_type=scrapy.Field()
    building_date=scrapy.Field()
    #xiaoqu_link = scrapy.Field()
    #scrapy_date = scrapy.Field()
    #origin = scrapy.Field()
