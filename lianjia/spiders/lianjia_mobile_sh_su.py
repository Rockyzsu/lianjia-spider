# coding: utf-8
import json
import re,time,os
import requests
import datetime
import scrapy
from lianjia.items import LianjiaItem
from scrapy.conf import settings
from lianjia.spiders.fetch_info import get_city_link, fetch_cookie
from lianjia.spiders.mayi_proxy_header import mayiproxy

#移动端 获取上海，苏州的小区
class Lianjia_Spider(scrapy.Spider):
    name='lianjia_m_sh'
    allowed_domains=['soa.dooioo.com']

    def __init__(self,city=None,*args, **kwargs):
        super(Lianjia_Spider,self).__init__(*args, **kwargs)
        self.city = city
        self.start_urls = [
            'http://soa.dooioo.com/api/v4/online/house/xiaoqu/search?access_token=7poanTTBCymmgE0FOn1oKp&channel=xiaoqu&cityCode=%s&client=wap&limit_count=20&limit_offset=0' %self.city]

        with open('city_name.txt','r') as city_fp:
            city_list=json.load(city_fp)

        self.city_name = city_list[self.city]
        with open('citys_count.txt','r') as fp_city_count:
            citys_count=json.load(fp_city_count)

        with open('lianjia_cookie_m.txt','r') as fp:
            self.cookie=json.dumps(fp)

        self.xiaoqu_count =citys_count[self.city]
        self.date = datetime.date.today()

        self.headers= {
            'Host': 'soa.dooioo.com',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Pragma': 'no-cache',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'User-Agent': 'UCWEB/2.0 (Linux; U; Adr 2.3; zh-CN; MI-ONEPlus) U2/1.0.0 UCBrowser/8.6.0.199 U2/1.0.0 Mobile',
            'X-Requested-With': 'XMLHttpRequest'
        }

        #self.cookie={'ubt_load_interval_b': '1503971694981', 'lj-ss': '5bd2bc45dbdf0644d704777dc2075366', 'Hm_lpvt_9152f8221cb6243a53c83b956842be8a': '1503997546', 'ubtd': '2', 'ubta': '3154866423.3241223259.1503971686808.1503971686808.1503971695039.2', 'ubtc': '3154866423.3241223259.1503971695041.0EF45810F9672DC3BD68868B080BCCEE', 'CNZZDATA1254525948': '145009446-1503633660-%7C1503995449', 'select_nation': '1', '_gid': 'GA1.2.2040440312.1503909104', 'CNZZDATA1253491255': '851767322-1503638199-%7C1503992440', 'gr_user_id': '4571568e-96d5-467c-ad95-9dd1f55471e1', '_ga': 'GA1.2.331020171.1503638699', '__xsptplus696': '696.1.1503971687.1503971695.2%234%7C%7C%7C%7C%7C%23%23fcZh1fCVH7j7doKzh4kC96wk_XE7Y965%23', 'lianjia_uuid': 'c6a7836e-cf96-45ae-96e5-6fdb2def9fb7', 'UM_distinctid': '15e17d9bbf960c-08e33a5d4e4891-4d015463-1fa400-15e17d9bbfa300', 'select_city': '441900', 'Hm_lvt_9152f8221cb6243a53c83b956842be8a': '1503638699'}

        self.meta = {
            'dont_redirect': True,  # 禁止网页重定向
            'handle_httpstatus_list': [301, 302]  # 对哪些异常返回进行处理
        }

        self.crawl_date = self.date = datetime.date.today()
        self.price_month='2017-07'

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
        # 上海和苏州的每一页20个
        for i in range(0,self.xiaoqu_count+40,20):
            url='http://soa.dooioo.com/api/v4/online/house/xiaoqu/search?access_token=7poanTTBCymmgE0FOn1oKp&channel=xiaoqu&cityCode=%s&client=wap&limit_count=20&limit_offset=%d' %(self.city,i)
            yield scrapy.Request(url=url,callback=self.parse_body,headers=self.headers)

    def parse_body(self,response):
        # response is json string
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

            address=i['propertyAddress'].strip()
            items['city_name'] = self.city_name
            items['location']=address
            price_detail={'price':price,'origin':'LJ','crawl_date':self.crawl_date}

            items['building_type'] = building_type
            items['building_date'] = building_year
            price_list=[]
            price_list.append(price_detail)
            price_dict = {self.price_month: price_list }
            items['price']=price_dict
            yield items
