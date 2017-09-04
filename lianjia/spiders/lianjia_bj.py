# coding: utf-8
import json
import re, time
import requests
import datetime
from lxml import etree
import scrapy
from lianjia.items import LianjiaItem
from scrapy.conf import settings
from lianjia.spiders.fetch_info import get_city_link, fetch_cookie, getXiaoquCount
from lianjia.spiders.mayi_proxy_header import mayiproxy


class Lianjia_Spider(scrapy.Spider):
    name = 'lianjia_web_bj'
    allowed_domains = ['lianjia.com']

    def __init__(self):
        self.date = datetime.date.today()
        # self.mayi_proxy, self.authHeader=mayiproxy()
        # 页面结构不同的有 北京 天津
        self.city = 'qd'
        self.city_name = '青岛'
        self.city_count = 3700
        self.headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Accept-Encoding': 'gzip, deflate, sdch',
                        'Accept-Language': 'zh-CN,zh;q=0.8',
                        'Connection': 'keep-alive',
                        'Upgrade-Insecure-Requests': '1',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'
                        }

        self.headers['Host'] = '%s.lianjia.com' % self.city
        self.cookie = {'ubt_load_interval_b': '1504165854069', 'all-lj': '6341ae6e32895385b04aae0cf3d794b0',
                       '_jzqa': '1.1378702697002941000.1504062784.1504162491.1504164572.7', '_jzqc': '1',
                       '_jzqb': '1.20.10.1504164572.1', '_qzjto': '16.4.0',
                       'Hm_lpvt_9152f8221cb6243a53c83b956842be8a': '1504169192', '_jzqckmp': '1',
                       '_smt_uid': '59a62d3f.3df2aef3', 'gr_user_id': '4571568e-96d5-467c-ad95-9dd1f55471e1',
                       '_jzqx': '1.1504062784.1504090314.3.jzqsr',
                       'CNZZDATA1255849469': '590735468-1504057966-null%7C1504167391', 'cityCode': 'sh',
                       '_ga': 'GA1.2.331020171.1503638699',
                       'CNZZDATA1254525948': '1531358740-1504060252-null%7C1504168464', 'select_nation': '1',
                       '_qzja': '1.218613373.1504062783783.1504164602018.1504166641481.1504169184377.1504169192487.0.0.0.44.7',
                       '_qzjc': '1', '_qzjb': '1.1504166641480.6.0.0.0',
                       'UM_distinctid': '15e17d9bbf960c-08e33a5d4e4891-4d015463-1fa400-15e17d9bbfa300',
                       'select_city': '440300', 'CNZZDATA1255633284': '355134272-1504060008-null%7C1504166449',
                       'lianjia_ssid': '5d09f424-3ea5-4240-ad81-024db2a8379b',
                       'CNZZDATA1255604082': '1601457208-1504060276-null%7C1504166658', 'ubtd': '29',
                       'ubta': '2299869246.3241223259.1503971686808.1504165855073.1504165862464.29',
                       'ubtc': '2299869246.3241223259.1504165862465.092EC81127748E6E91BE9ED24C39F495',
                       '_gid': 'GA1.2.2040440312.1503909104',
                       '__xsptplus696': '696.6.1504164644.1504165854.10%234%7C%7C%7C%7C%7C%23%23NTqr6t6GiZMyZVzgpXGicjWjL29L2Uan%23',
                       'lianjia_uuid': 'c6a7836e-cf96-45ae-96e5-6fdb2def9fb7',
                       'Hm_lvt_9152f8221cb6243a53c83b956842be8a': '1503638699'}

        self.meta = {
            'dont_redirect': True,  # 禁止网页重定向
            'handle_httpstatus_list': [301, 302]  # 对哪些异常返回进行处理
        }

        self.crawl_date = datetime.datetime.now().strftime("%Y-%m-%d")
        self.price_month = '2017-07'

    def start_requests(self):
        start_url = 'https://%s.lianjia.com/xiaoqu/' % self.city
        yield scrapy.Request(url=start_url, headers=self.headers, cookies=self.cookie)

    def parse(self, response):

        pages = (self.city_count + 31) / 30
        for i in range(1, pages + 3):
            url = 'https://%s.lianjia.com/xiaoqu/pg%dcro21/' % (self.city, i)
            print url
            self.headers['Referer'] = url
            yield scrapy.Request(url=url, callback=self.parse_body, headers=self.headers, cookies=self.cookie)

    def parse_body(self, response):

        print response.url
        city_name = self.city_name
        content = response.body
        tree = etree.HTML(content)
        nodes = tree.xpath('//ul[@class="listContent"]/li')
        print  "len : ", len(nodes)
        for node in nodes:
            items = LianjiaItem()
            name = node.xpath('.//div[@class="title"]/a/text()')[0]
            items['name'] = name
            try:
                position = node.xpath('.//div[@class="positionInfo"]/a/text()')
                address = position[0] + position[1]
            except:
                address = 'NA'
            print address
            items['location'] = address
            items['city_name'] = city_name
            try:
                text_content = node.xpath('.//div[@class="positionInfo"]/text()')
                # print len(build_date)

                detail = text_content[3].split('/')
                # 除去北京，北京的页面会多一个小区结构
                building_date = detail[-1].strip()
                building_type = detail[1].strip()
                if len(building_type)==0:
                    building_type='未知年建成'
                '''
                for k, i in enumerate(detail):
                    print k, i

                if len(detail) == 4:
                    buiding_type = detail[1].strip() + detail[3].strip()
                    build_date = detail[3].strip()
                elif len(detail) == 3:
                    buiding_type = detail[1].strip()

                    build_date = detail[2].strip()
                '''
            except:
                building_date = '未知年建成'
                building_type='NA'
            items['building_date'] = building_date
            items['building_type'] = building_type
            # details = desc.split()
            price_t = node.xpath('.//div[@class="totalPrice"]/span/text()')[0]

            p = re.findall('\d+', price_t)
            if len(p) != 0:
                price = int(price_t)
            else:
                price = '均价未知'
            print price
            price_detail = {'price': price, 'origin': 'LJ', 'crawl_date': self.crawl_date}
            price_list = []
            price_list.append(price_detail)
            price_dict = {self.price_month: price_list}
            items['price'] = price_dict
            yield items

    # 北京的页面元素较多
    def parse_body_bj(self, response):

        print response.url
        city_name = self.city_name
        content = response.body
        tree = etree.HTML(content)
        nodes = tree.xpath('//ul[@class="listContent"]/li')
        print  "len : ", len(nodes)
        for node in nodes:
            items = LianjiaItem()
            name = node.xpath('.//div[@class="title"]/a/text()')[0]
            items['name'] = name
            try:
                position = node.xpath('.//div[@class="positionInfo"]/a/text()')
                address = position[0] + position[1]
            except:
                address = 'NA'
            print address
            items['location'] = address
            items['city_name'] = city_name
            try:
                text_content = node.xpath('.//div[@class="positionInfo"]/text()')
                # print len(build_date)

                detail = text_content[3].split('/')
                # 除去北京，北京的页面会多一个小区结构
                building_date = detail[1].strip()
                building_type = "NA"
                '''
                for k, i in enumerate(detail):
                    print k, i

                if len(detail) == 4:
                    buiding_type = detail[1].strip() + detail[3].strip()
                    build_date = detail[3].strip()
                elif len(detail) == 3:
                    buiding_type = detail[1].strip()

                    build_date = detail[2].strip()
                '''
            except:
                building_date = '未知年建成'
            items['building_date'] = building_date
            items['building_type'] = building_type
            # details = desc.split()
            price_t = node.xpath('.//div[@class="totalPrice"]/span/text()')[0]

            p = re.findall('\d+', price_t)
            if len(p) != 0:
                price = int(price_t)
            else:
                price = '均价未知'
            print price
            price_detail = {'price': price, 'origin': 'LJ', 'crawl_date': self.crawl_date}
            price_list = []
            price_list.append(price_detail)
            price_dict = {self.price_month: price_list}
            items['price'] = price_dict
            yield items