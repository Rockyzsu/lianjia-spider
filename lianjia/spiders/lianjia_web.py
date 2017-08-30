# coding: utf-8
import json
import re,time
import requests
import datetime
from lxml import etree
import scrapy
from lianjia.items import LianjiaItem
from scrapy import log
from scrapy.conf import settings
from lianjia.spiders.fetch_info import get_city_link, fetch_cookie,getXiaoquCount
from lianjia.spiders.mayi_proxy_header import mayiproxy
class Lianjia_Spider(scrapy.Spider):
    name='lianjia_web'
    allowed_domains=['m.lianjia.com']

    start_urls=[
                'https://m.lianjia.com/sz/xiaoqu/',
                ]


    def __init__(self):
        self.date = datetime.date.today()
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
        self.city_link=get_city_link()
        #self.city_count=getXiaoquCount()
        self.city_count=json.load(open('city_count.txt'))
        self.cookie=fetch_cookie()
        self.meta = {
            'dont_redirect': True,  # 禁止网页重定向
            'handle_httpstatus_list': [301, 302]  # 对哪些异常返回进行处理
        }

        self.crawl_date = datetime.datetime.now().strftime("%Y-%m-%d")
        self.price_month='2017-07'

    def start_requests(self):
        '''
        for city in self.city_link:
            #print "city link" , city
            yield scrapy.Request(url=city,headers=self.headers,cookies=self.cookie)
            #time.sleep(10)
        '''
        url='https://sz.lianjia.com/xiaoqu/pg1cro21/'
        yield scrapy.Request(url=url,headers=self.headers,cookies=self.cookie)

    '''
    # 获取城市的小区数目
    def getXiaoquCount(self):
        city_count={}
        for city in self.city_link:
            print city
            city_code=city.split('/')[3]
            request_url = city+'xiaoqu/pg1/?_t=1'
            r=requests.get(url=request_url,headers=self.headers)
            print r
            xiaoqu_count = re.findall(r'\\"total\\":(\d+)}', r.text)[0]
            print "xiaoqu count",xiaoqu_count
            city_count[city_code]=int(xiaoqu_count)
        return city_count
    '''
    def parse(self, response):
        city_url=response.url
        #print city_url
        xiaoqu_count=city_url.split('/')[3]
        #count=self.city_count[xiaoqu_count]
        #count=100
        pages=(4833+25)/25

        for i in range(1,pages):
            url=city_url+'pg%d/?_t=1'  %i
            print "xiaoqu link ", url
            yield scrapy.Request(url=url,callback=self.parse_body,headers=self.headers,cookies=self.cookie)

    def parse_body(self,response):
        #date=self.date
        # 如何转换python datetime 到mongodb ？
        # response is json string
        print response.url

        js = json.loads(response.body)
        body = js['body']
        p = re.compile('"cur_city_name":"(.*?)"')
        city_name = p.findall(js['args'])[0].decode('unicode_escape')
        tree = etree.HTML(body)
        nodes = tree.xpath('//li[@class="pictext"]')
        log.msg(len(nodes), level=log.INFO)
        for node in nodes:
            items = LianjiaItem()
            #xiaoqu_url =node.xpath('.//a[@class="flexbox post_ulog"]/@href')[0]
            #items['xiaoqu_link']=xiaoqu_url
            name = node.xpath('.//div[@class="item_list"]/div[@class="item_main"]/text()')[0]
            items['name'] = name
            desc = node.xpath('.//div[@class="item_list"]/div[@class="item_other text_cut"]/text()')[0]
            items['city_name'] = city_name
            details = desc.split()
            if len(details)==3:
                #for detail in details:
                items['location'] = details[0]
                items['building_type'] = details[1]
                items['building_date'] = details[2]
            elif len(details)==2:
                items['location'] = details[0]
                items['building_type'] = "NA"
                items['building_date'] = details[1]
            elif len(details)==1:
                items['location'] = details[0]
                items['building_type'] = "NA"
                items['building_date'] = 'NA'
            else:
                items['location'] = 'NA'
                items['building_type'] = "NA"
                items['building_date'] = 'NA'
            price_t = node.xpath('.//div[@class="item_list"]/div[@class="item_minor"]/span/em/text()')[0]
            p=re.findall('\d+',price_t)
            if len(p)!=0:
                price = int(price_t)
            else:
                price = '均价未知'
            #items['scrapy_date'] = scrapy_date
            #items['origin']='LJ'
            price_detail={'price':price,'origin':'LJ','crawl_date':self.crawl_date}

            price_list=[]
            price_list.append(price_detail)
            price_dict = {self.price_month: price_list }
            items['price']=price_dict
            #print 'type of items : ',type(items)
            log.msg(items, level=log.INFO)
            yield items