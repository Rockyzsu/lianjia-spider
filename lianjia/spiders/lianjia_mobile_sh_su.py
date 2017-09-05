# coding: utf-8
import json
import re, time, os
import requests
import datetime
import scrapy
from lianjia.items import LianjiaItem
from scrapy.conf import settings
from lianjia.spiders.fetch_info import get_city_link, fetch_cookie
from lianjia.spiders.mayi_proxy_header import mayiproxy


# 移动端 获取上海，苏州的小区
class Lianjia_Spider_Mobile(scrapy.Spider):
    name = 'lianjia_m_sh_su'
    allowed_domains = ['soa.dooioo.com']

    def __init__(self, city=None, *args, **kwargs):
        super(Lianjia_Spider_Mobile, self).__init__(*args, **kwargs)
        self.city = city
        self.start_urls = ['http://soa.dooioo.com/api/v4/online/house/xiaoqu/search?access_token=\
        7poanTTBCymmgE0FOn1oKp&channel=xiaoqu&cityCode=%s&client=wap&limit_count=20&limit_offset=0' % self.city]

        with open('city_name.txt', 'r') as city_fp:
            city_list = json.load(city_fp)

        self.city_name = city_list[self.city]
        with open('citys_count.txt', 'r') as fp_city_count:
            citys_count = json.load(fp_city_count)

        self.xiaoqu_count = citys_count[self.city]

        self.headers = {
            'Host': 'soa.dooioo.com',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Pragma': 'no-cache',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'User-Agent': 'UCWEB/2.0 (Linux; U; Adr 2.3; zh-CN; MI-ONEPlus)\
             U2/1.0.0 UCBrowser/8.6.0.199 U2/1.0.0 Mobile',
            'X-Requested-With': 'XMLHttpRequest'
        }
        # 移动端的上海苏州不需要cookies
        self.crawl_date = datetime.datetime.now().strftime('%Y-%m-%d')
        self.price_month = '2017-07'


    def parse(self, response):
        # 上海和苏州的每一页20个
        for i in range(0, self.xiaoqu_count + 40, 20):
            url = 'http://soa.dooioo.com/api/v4/online/house/xiaoqu/search?access_token=\
            7poanTTBCymmgE0FOn1oKp&channel=xiaoqu&cityCode=%s&client=wap&limit_count=20&limit_offset=%d' % (
            self.city, i)
            yield scrapy.Request(url=url, callback=self.parse_body, headers=self.headers)

    def parse_body(self, response):
        # response is json string
        js = json.loads(response.body)
        body = js['data']['list']
        print "len of body", len(body)
        for element in body:
            items = LianjiaItem()

            if element.has_key('referAvgPrice'):
                price = int(element['referAvgPrice'])
            else:
                price = "NA"

            if element.has_key('houseType'):
                building_type = element['houseType']
            else:
                building_type = 'NA'

            if element.has_key('completeYear'):
                building_year = element['completeYear']
            else:
                building_year = 'NA'

            if element.has_key('propertyName'):
                items['name'] = element['propertyName']
            else:
                items['name'] = 'NA'

            address = element['propertyAddress'].strip()
            items['city_name'] = self.city_name
            items['location'] = address
            price_detail = {'price': price, 'origin': 'LJ', 'crawl_date': self.crawl_date}

            items['building_type'] = building_type
            items['building_date'] = building_year
            price_list = []
            price_list.append(price_detail)
            price_dict = {self.price_month: price_list}
            items['price'] = price_dict
            yield items
