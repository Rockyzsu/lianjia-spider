# coding: utf-8
import json
import re
import requests
import datetime
from lxml import etree
import scrapy
from lianjia.items import LianjiaItem
from scrapy import log
from scrapy.conf import settings
from lianjia.spiders.fetch_info import get_city_link
from lianjia.spiders.mayi_proxy_header import mayiproxy
class Lianjia_Spider(scrapy.Spider):
    name='lianjia'
    allowed_domains=['m.lianjia.com']
    #start_urls=['https://m.lianjia.com/hz/xiaoqu/pg1/?_t=1',]

    '''
    def start_requests(self):
        url='https://m.lianjia.com/hz/xiaoqu/pg1/?_t=1'
    '''
    def __init__(self):
        self.date = datetime.date.today()
        with open('lianjia_cookie.txt','r') as fp:
            self.cookie=fp.read().strip()

        #self.mayi_proxy, self.authHeader=mayiproxy()
        self.headers= {
            'Host': 'm.lianjia.com',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Pragma': 'no-cache',
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
            'User-Agent': 'UCWEB/2.0 (Linux; U; Adr 2.3; zh-CN; MI-ONEPlus) U2/1.0.0 UCBrowser/8.6.0.199 U2/1.0.0 Mobile',
            'X-Requested-With': 'XMLHttpRequest'
            #'Proxy-Authorization': self.authHeader
        }
        #self.city_link=get_city_link()
        #self.city_count=self.getXiaoquCount()
        #self.cookie=settings['cookie']
        self.cookie={'_gat_new_global': '1', 'lj-ss': '5bd2bc45dbdf0644d704777dc2075366', '_gat_global': '1', '_gat_new': '1', 'Hm_lpvt_9152f8221cb6243a53c83b956842be8a': '1503912523', '_gat_past': '1', '_ga': 'GA1.2.331020171.1503638699', '_gat': '1', 'CNZZDATA1254525948': '145009446-1503633660-%7C1503908541', 'lianjia_ssid': '290ce12b-c434-4782-9b1a-06c450c2dbb3', 'select_nation': '1', '_gid': 'GA1.2.2040440312.1503909104', 'CNZZDATA1253491255': '851767322-1503638199-%7C1503907203', 'lianjia_uuid': 'c6a7836e-cf96-45ae-96e5-6fdb2def9fb7', 'UM_distinctid': '15e17d9bbf960c-08e33a5d4e4891-4d015463-1fa400-15e17d9bbfa300', 'select_city': '440300', 'Hm_lvt_9152f8221cb6243a53c83b956842be8a': '1503638699'}

        self.meta = {
            'dont_redirect': True,  # 禁止网页重定向
            'handle_httpstatus_list': [301, 302]  # 对哪些异常返回进行处理
        }

    def start_requests(self):
        '''
        for city in self.city_link:
            yield scrapy.Request(url=city,headers=self.headers)
        '''
        url='https://m.lianjia.com/dg/xiaoqu'
        yield scrapy.Request(url=url,headers=self.headers,cookies=self.cookie)
    # 获取城市的小区数目
    def getXiaoquCount(self):
        city_count={}
        for city in self.city_link:
            print city
            city_code=city.split('/')[3]
            request_url = city+'xiaoqu/pg1/?_t=1'
            r=requests.get(url=request_url,headers=self.headers,cookies=self.cookie)
            print r
            xiaoqu_count = re.findall(r'\\"total\\":(\d+)}', r.text)[0]
            print "xiaoqu count",xiaoqu_count
            city_count[city_code]=int(xiaoqu_count)
        return city_count

    def parse(self, response):
        city_url=response.url

        #xiaoqu_count=city_url.split('/')[3]
        #count=self.city_count[xiaoqu_count]
        count=1032
        pages=(count+25)/25

        for i in range(1,pages):
            url=city_url+'/pg%d/?_t=1'  %i
            yield scrapy.Request(url=url,callback=self.parse_body,headers=self.headers,cookies=self.cookie)

    def parse_body(self,response):
        #date=self.date
        # 如何转换python datetime 到mongodb ？
        # response is json string
        print response.url
        date=datetime.datetime.now().strftime("%Y-%m-%d")
        js = json.loads(response.body)
        body = js['body']
        p = re.compile('"cur_city_name":"(.*?)"')
        city_name = p.findall(js['args'])[0].decode('unicode_escape')
        tree = etree.HTML(body)
        nodes = tree.xpath('//li[@class="pictext"]')
        log.msg(len(nodes), level=log.INFO)
        for node in nodes:
            items = LianjiaItem()
            xiaoqu_url =node.xpath('.//a[@class="flexbox post_ulog"]/@href')[0]
            items['xiaoqu_link']=xiaoqu_url
            name = node.xpath('.//div[@class="item_list"]/div[@class="item_main"]/text()')[0]
            items['name'] = name
            desc = node.xpath('.//div[@class="item_list"]/div[@class="item_other text_cut"]/text()')[0]
            items['city_name'] = city_name
            details = desc.split()
            items['location'] = details[0]
            items['building_type'] = details[1]
            items['building_date'] = details[2]
            price = node.xpath('.//div[@class="item_list"]/div[@class="item_minor"]/span/em/text()')[0]
            p=re.search('\d+',price)
            if p:
                items['price'] = int(price)
            else:
                items['price'] = price
            items['scrapy_date'] = date
            items['origin']='链家'
            #print 'type of items : ',type(items)
            log.msg(items, level=log.INFO)
            yield items