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
from lianjia.spiders.fetch_info import get_city_link, fetch_cookie
from lianjia.spiders.mayi_proxy_header import mayiproxy
class Lianjia_Spider(scrapy.Spider):
    name='lianjia_sh'
    allowed_domains=['soa.dooioo.com']
    #start_urls=['http://soa.dooioo.com/api/v4/online/house/xiaoqu/search?access_token=7poanTTBCymmgE0FOn1oKp&channel=xiaoqu&cityCode=sh&client=wap&limit_count=20&limit_offset=0',]
    start_urls=['http://soa.dooioo.com/api/v4/online/house/xiaoqu/search?access_token=7poanTTBCymmgE0FOn1oKp&channel=xiaoqu&cityCode=su&client=wap&limit_count=20&limit_offset=0']
    '''
    def start_requests(self):
        url='https://m.lianjia.com/wh/xiaoqu/pg1/?_t=1'
    '''
    def __init__(self):
        self.date = datetime.date.today()
        with open('lianjia_cookie.txt','r') as fp:
            self.cookie=fp.read().strip()

        #self.mayi_proxy, self.authHeader=mayiproxy()
        self.headers= {
            'Host': 'soa.dooioo.com',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Pragma': 'no-cache',
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
        #self.cookie={'_gat_new_global': '1', 'lj-ss': '5bd2bc45dbdf0644d704777dc2075366', '_gat_global': '1', '_gat_new': '1', 'Hm_lpvt_9152f8221cb6243a53c83b956842be8a': '1503912523', '_gat_past': '1', '_ga': 'GA1.2.331020171.1503638699', '_gat': '1', 'CNZZDATA1254525948': '145009446-1503633660-%7C1503908541', 'lianjia_ssid': '290ce12b-c434-4782-9b1a-06c450c2dbb3', 'select_nation': '1', '_gid': 'GA1.2.2040440312.1503909104', 'CNZZDATA1253491255': '851767322-1503638199-%7C1503907203', 'lianjia_uuid': 'c6a7836e-cf96-45ae-96e5-6fdb2def9fb7', 'UM_distinctid': '15e17d9bbf960c-08e33a5d4e4891-4d015463-1fa400-15e17d9bbfa300', 'select_city': '440300', 'Hm_lvt_9152f8221cb6243a53c83b956842be8a': '1503638699'}
        #self.cookie={'_gat_new_global': '1', 'lj-ss': '5bd2bc45dbdf0644d704777dc2075366', '_gat_global': '1', '_gat_new': '1', 'Hm_lpvt_9152f8221cb6243a53c83b956842be8a': '1503920035', '_gat_past': '1', '_ga': 'GA1.2.331020171.1503638699', '_gat': '1', 'CNZZDATA1254525948': '145009446-1503633660-%7C1503919341', 'lianjia_ssid': 'e07f3016-cad2-4f82-96f5-516af563669e', 'select_nation': '1', '_gid': 'GA1.2.2040440312.1503909104', 'CNZZDATA1253491255': '851767322-1503638199-%7C1503914876', 'lianjia_uuid': 'c6a7836e-cf96-45ae-96e5-6fdb2def9fb7', 'UM_distinctid': '15e17d9bbf960c-08e33a5d4e4891-4d015463-1fa400-15e17d9bbfa300', 'select_city': '441900', 'Hm_lvt_9152f8221cb6243a53c83b956842be8a': '1503638699'}
        #self.cookie={'lianjia_uuid': 'c6a7836e-cf96-45ae-96e5-6fdb2def9fb7', '_gat_new': '1', 'lj-ss': '5bd2bc45dbdf0644d704777dc2075366', 'Hm_lpvt_9152f8221cb6243a53c83b956842be8a': '1503984016', 'select_city': '500000', 'CNZZDATA1253491255': '851767322-1503638199-%7C1503981640', 'gr_user_id': '4571568e-96d5-467c-ad95-9dd1f55471e1', 'ubt_load_interval_b': '1503971694981', '_gat_past': '1', '_ga': 'GA1.2.331020171.1503638699', 'CNZZDATA1254525948': '145009446-1503633660-%7C1503984153', 'select_nation': '1', 'UM_distinctid': '15e17d9bbf960c-08e33a5d4e4891-4d015463-1fa400-15e17d9bbfa300', '_gat': '1', '_gat_new_global': '1', 'lianjia_ssid': '343c0faf-c443-4673-b900-5c05298bd28a', 'ubtd': '2', 'ubta': '3154866423.3241223259.1503971686808.1503971686808.1503971695039.2', 'ubtc': '3154866423.3241223259.1503971695041.0EF45810F9672DC3BD68868B080BCCEE', '_gid': 'GA1.2.2040440312.1503909104', '__xsptplus696': '696.1.1503971687.1503971695.2%234%7C%7C%7C%7C%7C%23%23fcZh1fCVH7j7doKzh4kC96wk_XE7Y965%23', '_gat_global': '1', 'Hm_lvt_9152f8221cb6243a53c83b956842be8a': '1503638699'}
        #local_cooki=fetch_cookie()
        #self.cookie={'lianjia_uuid': 'c6a7836e-cf96-45ae-96e5-6fdb2def9fb7', '_gat_new': '1', 'lj-ss': '5bd2bc45dbdf0644d704777dc2075366', 'Hm_lpvt_9152f8221cb6243a53c83b956842be8a': '1503997546', 'select_city': '441900', 'CNZZDATA1253491255': '851767322-1503638199-%7C1503992440', 'gr_user_id': '4571568e-96d5-467c-ad95-9dd1f55471e1', 'ubt_load_interval_b': '1503971694981', '_gat_past': '1', '_ga': 'GA1.2.331020171.1503638699', 'CNZZDATA1254525948': '145009446-1503633660-%7C1503995449', 'select_nation': '1', 'UM_distinctid': '15e17d9bbf960c-08e33a5d4e4891-4d015463-1fa400-15e17d9bbfa300', '_gat': '1', '_gat_new_global': '1', 'lianjia_ssid': 'bc9efc9f-e684-48a9-ba85-00445efd9b8e', 'ubtd': '2', 'ubta': '3154866423.3241223259.1503971686808.1503971686808.1503971695039.2', 'ubtc': '3154866423.3241223259.1503971695041.0EF45810F9672DC3BD68868B080BCCEE', '_gid': 'GA1.2.2040440312.1503909104', '__xsptplus696': '696.1.1503971687.1503971695.2%234%7C%7C%7C%7C%7C%23%23fcZh1fCVH7j7doKzh4kC96wk_XE7Y965%23', '_gat_global': '1', 'Hm_lvt_9152f8221cb6243a53c83b956842be8a': '1503638699'}
        #self.cookie=local_cooki
        self.cookie={'ubt_load_interval_b': '1503971694981', 'lj-ss': '5bd2bc45dbdf0644d704777dc2075366', 'Hm_lpvt_9152f8221cb6243a53c83b956842be8a': '1503997546', 'ubtd': '2', 'ubta': '3154866423.3241223259.1503971686808.1503971686808.1503971695039.2', 'ubtc': '3154866423.3241223259.1503971695041.0EF45810F9672DC3BD68868B080BCCEE', 'CNZZDATA1254525948': '145009446-1503633660-%7C1503995449', 'select_nation': '1', '_gid': 'GA1.2.2040440312.1503909104', 'CNZZDATA1253491255': '851767322-1503638199-%7C1503992440', 'gr_user_id': '4571568e-96d5-467c-ad95-9dd1f55471e1', '_ga': 'GA1.2.331020171.1503638699', '__xsptplus696': '696.1.1503971687.1503971695.2%234%7C%7C%7C%7C%7C%23%23fcZh1fCVH7j7doKzh4kC96wk_XE7Y965%23', 'lianjia_uuid': 'c6a7836e-cf96-45ae-96e5-6fdb2def9fb7', 'UM_distinctid': '15e17d9bbf960c-08e33a5d4e4891-4d015463-1fa400-15e17d9bbfa300', 'select_city': '441900', 'Hm_lvt_9152f8221cb6243a53c83b956842be8a': '1503638699'}

        self.meta = {
            'dont_redirect': True,  # 禁止网页重定向
            'handle_httpstatus_list': [301, 302]  # 对哪些异常返回进行处理

        }

        self.crawl_date = datetime.datetime.now().strftime("%Y-%m-%d")
        self.price_month='2017-07'
    '''
    def start_requests(self):

        #for city in self.city_link:
            #yield scrapy.Request(url=city,headers=self.headers,cookies=self.cookie)
            #time.sleep(10)

        url='https://m.lianjia.com/km/'
        yield scrapy.Request(url=url,headers=self.headers,cookies=self.cookie)
    '''
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
        #count=100
        pages=(1345+25)/25

        for i in range(0,27474,20):
            url='http://soa.dooioo.com/api/v4/online/house/xiaoqu/search?access_token=7poanTTBCymmgE0FOn1oKp&channel=xiaoqu&cityCode=sh&client=wap&limit_count=20&limit_offset=%d' %i
            yield scrapy.Request(url=url,callback=self.parse_body,headers=self.headers)

    def parse_body(self,response):
        #date=self.date
        # 如何转换python datetime 到mongodb ？
        # response is json string
        print response.url
        city_name='上海'
        js = json.loads(response.body)
        body = js['data']['list']
        print "len of body" , len(body)
        for i in body:
            items = LianjiaItem()

            if i.has_key('referAvgPrice'):
                price = int(i['referAvgPrice'])
            else:
                price="NA"

            if i.has_key('houseType'):
                building_type = i['houseType']
            else:
                building_type='NA'

            if i.has_key('completeYear'):
                building_year = i['completeYear']
            else:
                building_year='NA'

            if i.has_key('propertyName'):
                items['name'] = i['propertyName']
            else:
                items['name']='NA'


            items['city_name'] = city_name

            price_detail={'price':price,'origin':'LJ','crawl_date':self.crawl_date}

            items['building_type'] = building_type
            items['building_date'] = building_year
            price_list=[]
            price_list.append(price_detail)
            price_dict = {self.price_month: price_list }
            items['price']=price_dict
            #print 'type of items : ',type(items)
            log.msg(items, level=log.INFO)
            yield items
