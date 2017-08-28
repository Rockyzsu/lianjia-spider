# coding: utf-8
import json
import re
import requests
import datetime
from lxml import etree
import scrapy
from lianjia.items import LianjiaItem
from lianjia.spiders.fetch_info import get_city_link
from lianjia.spiders.mayi_proxy_header import mayiproxy


class Lianjia_Spider(scrapy.Spider):
    name = 'lianjia_proxy'
    allowed_domains = ['m.lianjia.com']
    # start_urls=['https://m.lianjia.com/hz/xiaoqu/pg1/?_t=1',]

    '''
    def start_requests(self):
        url='https://m.lianjia.com/hz/xiaoqu/pg1/?_t=1'
    '''

    def __init__(self):
        self.date = datetime.date.today()
        with open('lianjia_cookie.txt', 'r') as fp:
            self.cookie = fp.read().strip()

        self.mayi_proxy, self.authHeader = mayiproxy()
        self.headers = {
            'Host': 'm.lianjia.com',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Pragma': 'no-cache',
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
            'User-Agent': 'UCWEB/2.0 (Linux; U; Adr 2.3; zh-CN; MI-ONEPlus) U2/1.0.0 UCBrowser/8.6.0.199 U2/1.0.0 Mobile',
            'X-Requested-With': 'XMLHttpRequest',
            'Proxy-Authorization': self.authHeader
        }
        self.city_link = get_city_link()
        self.city_count = self.getXiaoquCount()

    def start_requests(self):
        for city in self.city_link:
            yield scrapy.Request(url=city, headers=self.headers, meta={'proxy': self.mayi_proxy['http']})

    # 获取城市的小区数目
    def getXiaoquCount(self):
        city_count = {}
        for city in self.city_link:
            print city
            city_code = city.split('/')[3]
            request_url = city + 'xiaoqu/pg1/?_t=1'
            r = requests.get(url=request_url, headers=self.headers,proxies=self.mayi_proxy)
            print r
            xiaoqu_count = re.findall(r'\\"total\\":(\d+)}', r.text)[0]
            print "xiaoqu count", xiaoqu_count
            city_count[city_code] = int(xiaoqu_count)
        return city_count

    def parse(self, response):
        city_url = response.url
        xiaoqu_count = city_url.split('/')[3]
        count = self.city_count[xiaoqu_count]
        pages = count / 25 + 1

        for i in range(1, pages):
            url = city_url + 'xiaoqu/pg%d/?_t=1' % i
            yield scrapy.Request(url=url, headers=self.headers, meta={'proxy': self.mayi_proxy['http']},
                                 callback=self.parse_body)

    def parse_body(self, response):
        # date=self.date
        # 如何转换python datetime 到mongodb ？
        # response is json string
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        js = json.loads(response.body)
        body = js['body']
        p = re.compile('"cur_city_name":"(.*?)"')
        city_name = p.findall(js['args'])[0].decode('unicode_escape')
        tree = etree.HTML(body)
        nodes = tree.xpath('//li[@class="pictext"]')
        for node in nodes:
            items = LianjiaItem()
            xiaoqu_url = node.xpath('.//a[@class="flexbox post_ulog"]/@href')[0]
            items['xiaoqu_link'] = xiaoqu_url
            name = node.xpath('.//div[@class="item_list"]/div[@class="item_main"]/text()')[0]
            items['name'] = name
            desc = node.xpath('.//div[@class="item_list"]/div[@class="item_other text_cut"]/text()')[0]
            items['city_name'] = city_name
            details = desc.split()
            items['location'] = details[0]
            items['building_type'] = details[1]
            items['building_date'] = details[2]
            price = node.xpath('.//div[@class="item_list"]/div[@class="item_minor"]/span/em/text()')[0]
            items['price'] = price
            items['scrapy_date'] = date
            items['origin'] = '链家'
            print 'type of items : ', type(items)
            yield items
