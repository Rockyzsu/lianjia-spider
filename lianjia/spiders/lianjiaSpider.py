# coding: utf-8
import json
from lxml import etree
import scrapy
from lianjia.items import LianjiaItem
class Lianjia_Spider(scrapy.Spider):
    name='lianjia'
    allowed_domains=['m.lianjia.com']
    start_urls=['']
    def parse(self, response):
        for i in range(1,10):
            url='https://m.lianjia.com/sz/xiaoqu/pg%d/?_t=1'  %i
            yield scrapy.Request(url=url,callback=self.parse_body)

    def parse_body(self,response):
        # response is json string
        js = json.loads(response.body)
        body = js['body']
        tree = etree.HTML(body)
        nodes = tree.xpath('//li[@class="pictext"]')
        for node in nodes:
            items = LianjiaItem()
            name = node.xpath('.//div[@class="item_list"]/div[@class="item_main"]/text()')[0]
            items['name'] = name
            desc = node.xpath('.//div[@class="item_list"]/div[@class="item_other text_cut"]/text()')[0]
            details = desc.split()
            items['location'] = details[0]
            items['building_type'] = details[1]
            items['building_date'] = details[2]
            price = node.xpath('.//div[@class="item_list"]/div[@class="item_minor"]/span/em/text()')[0]
            items['price'] = price
            yield items