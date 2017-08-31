# coding: utf-8
import json
import re, time
import requests
import datetime
from lxml import etree
import scrapy
from lianjia.items import LianjiaItem
from scrapy import log
from scrapy.conf import settings
#from lianjia.spiders.fetch_info import get_city_link, fetch_cookie, getXiaoquCount
#from lianjia.spiders.mayi_proxy_header import mayiproxy


class Lianjia_Spider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['m.lianjia.com']

    start_urls=[
                'https://m.lianjia.com/km/xiaoqu/pg1/?_t=1',
                ]


    def __init__(self):
        self.date = datetime.date.today()
        # self.mayi_proxy, self.authHeader=mayiproxy()
        #self.cookie={'sample_traffic_test': 'guide_card', 'lianjia_uuid': 'c6a7836e-cf96-45ae-96e5-6fdb2def9fb7', '_gat_new': '1', '_jzqa': '1.1378702697002941000.1504062784.1504083754.1504090314.4', '_jzqc': '1', '_jzqb': '1.3.10.1504090314.1', 'lj-ss': '5bd2bc45dbdf0644d704777dc2075366', 'Hm_lpvt_9152f8221cb6243a53c83b956842be8a': '1504091650', '_jzqckmp': '1', '_smt_uid': '59a62d3f.3df2aef3', 'CNZZDATA1253491255': '851767322-1503638199-%7C1504091020', 'gr_user_id': '4571568e-96d5-467c-ad95-9dd1f55471e1', '_jzqx': '1.1504062784.1504090314.3.jzqsr', 'ubt_load_interval_b': '1504076659297', '_gat_past': '1', 'lj-api': '9111950472618e41591b6800072ddacb', '_ga': 'GA1.2.331020171.1503638699', 'CNZZDATA1254525948': '145009446-1503633660-%7C1504087254', '_gat_dianpu_agent': '1', 'select_nation': '1', '_gat': '1', 'UM_distinctid': '15e17d9bbf960c-08e33a5d4e4891-4d015463-1fa400-15e17d9bbfa300', 'select_city': '441300', '_gat_new_global': '1', 'lianjia_ssid': 'bd082802-0db2-4698-84e5-b015007e18f3', 'ubtd': '19', 'ubta': '3154866423.3241223259.1503971686808.1504062380059.1504076659413.19', 'ubtc': '3154866423.3241223259.1504076659416.04775B09D4A0751F8665A61B54987A68', '_gid': 'GA1.2.2040440312.1503909104', '__xsptplus696': '696.5.1504076659.1504076659.1%234%7C%7C%7C%7C%7C%23%230CIWTVwbBidFOpEsVtab9KgnY2MeVIYe%23', '_gat_global': '1', 'Hm_lvt_9152f8221cb6243a53c83b956842be8a': '1503638699'}
        #cookie='lj-ss=5bd2bc45dbdf0644d704777dc2075366; lianjia_uuid=c6a7836e-cf96-45ae-96e5-6fdb2def9fb7; UM_distinctid=15e17d9bbf960c-08e33a5d4e4891-4d015463-1fa400-15e17d9bbfa300; gr_user_id=4571568e-96d5-467c-ad95-9dd1f55471e1; lj-api=9111950472618e41591b6800072ddacb; _jzqckmp=1; ubt_load_interval_b=1504076659297; ubta=3154866423.3241223259.1503971686808.1504062380059.1504076659413.19; ubtc=3154866423.3241223259.1504076659416.04775B09D4A0751F8665A61B54987A68; ubtd=19; __xsptplus696=696.5.1504076659.1504076659.1%234%7C%7C%7C%7C%7C%23%230CIWTVwbBidFOpEsVtab9KgnY2MeVIYe%23; sample_traffic_test=guide_card; select_nation=1; _jzqx=1.1504062784.1504090314.3.jzqsr=sz%2Efang%2Elianjia%2Ecom|jzqct=/.jzqsr=you%2Elianjia%2Ecom|jzqct=/hk; select_city=441300; _smt_uid=59a62d3f.3df2aef3; _jzqa=1.1378702697002941000.1504062784.1504083754.1504090314.4; _jzqc=1; _jzqb=1.3.10.1504090314.1; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1503638699; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1504091650; _ga=GA1.2.331020171.1503638699; _gid=GA1.2.2040440312.1503909104; CNZZDATA1254525948=145009446-1503633660-%7C1504087254; CNZZDATA1253491255=851767322-1503638199-%7C1504091020; lianjia_ssid=bd082802-0db2-4698-84e5-b015007e18f3'
        self.headers = {
            'Host': 'm.lianjia.com',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.8',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36',
            #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
            #'User-Agent': 'UCWEB/2.0 (Linux; U; Adr 2.3; zh-CN; MI-ONEPlus) U2/1.0.0 UCBrowser/8.6.0.199 U2/1.0.0 Mobile',
            'X-Requested-With': 'XMLHttpRequest'
            # 'Proxy-Authorization': self.authHeader
            #'Cookie':cookie
        }
        #self.city_link = get_city_link()
        # self.city_count=getXiaoquCount()
        #self.city_count = json.load(open('city_count.txt'))
        #self.cookie = fetch_cookie()
        #self.cookie={'ubt_load_interval_b': '1503971694981', 'lj-ss': '5bd2bc45dbdf0644d704777dc2075366', 'Hm_lpvt_9152f8221cb6243a53c83b956842be8a': '1503997546', 'ubtd': '2', 'ubta': '3154866423.3241223259.1503971686808.1503971686808.1503971695039.2', 'ubtc': '3154866423.3241223259.1503971695041.0EF45810F9672DC3BD68868B080BCCEE', 'CNZZDATA1254525948': '145009446-1503633660-%7C1503995449', 'select_nation': '1', '_gid': 'GA1.2.2040440312.1503909104', 'CNZZDATA1253491255': '851767322-1503638199-%7C1503992440', 'gr_user_id': '4571568e-96d5-467c-ad95-9dd1f55471e1', '_ga': 'GA1.2.331020171.1503638699', '__xsptplus696': '696.1.1503971687.1503971695.2%234%7C%7C%7C%7C%7C%23%23fcZh1fCVH7j7doKzh4kC96wk_XE7Y965%23', 'lianjia_uuid': 'c6a7836e-cf96-45ae-96e5-6fdb2def9fb7', 'UM_distinctid': '15e17d9bbf960c-08e33a5d4e4891-4d015463-1fa400-15e17d9bbfa300', 'select_city': '441900', 'Hm_lvt_9152f8221cb6243a53c83b956842be8a': '1503638699'}
        #self.cookies={'sample_traffic_test': 'guide_card', '_jzqa': '1.1378702697002941000.1504062784.1504083754.1504090314.4', '_jzqc': '1', '_jzqb': '1.3.10.1504090314.1', 'lj-ss': '5bd2bc45dbdf0644d704777dc2075366', 'Hm_lpvt_9152f8221cb6243a53c83b956842be8a': '1504092147', '_jzqckmp': '1', '_smt_uid': '59a62d3f.3df2aef3', 'CNZZDATA1253491255': '851767322-1503638199-%7C1504091020', 'gr_user_id': '4571568e-96d5-467c-ad95-9dd1f55471e1', '_jzqx': '1.1504062784.1504090314.3.jzqsr', 'ubt_load_interval_b': '1504076659297', 'lj-api': '9111950472618e41591b6800072ddacb', '_ga': 'GA1.2.331020171.1503638699', 'CNZZDATA1254525948': '145009446-1503633660-%7C1504087254', 'select_nation': '1', 'UM_distinctid': '15e17d9bbf960c-08e33a5d4e4891-4d015463-1fa400-15e17d9bbfa300', 'select_city': '441300', 'lianjia_ssid': 'bd082802-0db2-4698-84e5-b015007e18f3', 'ubtd': '19', 'ubta': '3154866423.3241223259.1503971686808.1504062380059.1504076659413.19', 'ubtc': '3154866423.3241223259.1504076659416.04775B09D4A0751F8665A61B54987A68', '_gid': 'GA1.2.2040440312.1503909104', '__xsptplus696': '696.5.1504076659.1504076659.1%234%7C%7C%7C%7C%7C%23%230CIWTVwbBidFOpEsVtab9KgnY2MeVIYe%23', 'lianjia_uuid': 'c6a7836e-cf96-45ae-96e5-6fdb2def9fb7', 'Hm_lvt_9152f8221cb6243a53c83b956842be8a': '1503638699'}
        #self.cookie={'lianjia_uuid': 'ca5a64ec-9cbe-4f31-8499-f06c3ea622da', '_gat_new': '1', '_jzqa': '1.206544328628398600.1503881786.1503881786.1503881786.1', 'lj-ss': '1e5c8b6bb356c2aabadd162c97341948', 'Hm_lpvt_9152f8221cb6243a53c83b956842be8a': '1504101536', '_gat': '1', '_smt_uid': '59a36a39.a7e32ae', 'CNZZDATA1253491255': '597282999-1503832971-%7C1504096420', 'gr_user_id': '9895cc06-d162-4985-b42c-0cc98cdee98f', '_gat_past': '1', '_ga': 'GA1.2.885541457.1503837305', 'CNZZDATA1254525948': '1758800946-1503835682-%7C1504096368', 'select_nation': '1', 'UM_distinctid': '15e23b039a53a7-0b6a06eff463b1-5c153d17-1fa400-15e23b039a68d1', 'select_city': '441300', '_gat_new_global': '1', 'lianjia_ssid': '9410766c-34bd-4115-a879-5b11375f9924', 'ubta': '3154866423.1593962235.1503840667336.1503845425552.1503845426709.19', '_gid': 'GA1.2.726828377.1504101487', '__xsptplus696': '696.2.1503843548.1503845425.16%234%7C%7C%7C%7C%7C%23%237HfP43631brEPPGQ4VLVKcfdTX7U_iad%23', '_gat_global': '1', 'Hm_lvt_9152f8221cb6243a53c83b956842be8a': '1503837305,1503881786,1504101487'}
        #self.headers['Cookie']=self.cookie
        self.cookie={'_jzqa': '1.206544328628398600.1503881786.1503881786.1503881786.1', 'lj-ss': '1e5c8b6bb356c2aabadd162c97341948', 'lianjia_ssid': '9410766c-34bd-4115-a879-5b11375f9924', 'Hm_lpvt_9152f8221cb6243a53c83b956842be8a': '1504102362', '_ga': 'GA1.2.885541457.1503837305', 'ubta': '3154866423.1593962235.1503840667336.1503845425552.1503845426709.19', 'CNZZDATA1254525948': '1758800946-1503835682-%7C1504098054', '_smt_uid': '59a36a39.a7e32ae', 'select_nation': '1', '_gid': 'GA1.2.726828377.1504101487', 'CNZZDATA1253491255': '597282999-1503832971-%7C1504101820', 'gr_user_id': '9895cc06-d162-4985-b42c-0cc98cdee98f', '__xsptplus696': '696.2.1503843548.1503845425.16%234%7C%7C%7C%7C%7C%23%237HfP43631brEPPGQ4VLVKcfdTX7U_iad%23', 'lianjia_uuid': 'ca5a64ec-9cbe-4f31-8499-f06c3ea622da', 'UM_distinctid': '15e23b039a53a7-0b6a06eff463b1-5c153d17-1fa400-15e23b039a68d1', 'select_city': '441300', 'Hm_lvt_9152f8221cb6243a53c83b956842be8a': '1503837305,1503881786,1504101487'}
        self.crawl_date = datetime.datetime.now().strftime("%Y-%m-%d")
        self.price_month = '2017-07'

    #def start_requests(self):
        '''
        for city in self.city_link:
            #print "city link" , city
            yield scrapy.Request(url=city,headers=self.headers,cookies=self.cookie)
            #time.sleep(10)
        '''
        #url = 'https://m.lianjia.com/hui/xiaoqu/pg1/?_t=1'
        #yield scrapy.Request(url=url, headers=self.headers,cookies=self.cookie)



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
        city_url = response.url
        # print city_url
        # xiaoqu_count=city_url.split('/')[3]
        # count=self.city_count[xiaoqu_count]
        # count=100
        pages = (1348 + 25) / 25

        for i in range(1, pages+1):
            base_url='https://m.lianjia.com/km/xiaoqu/pg%d/' %i
            url = base_url+'?_t=1'
            print "xiaoqu link ", url
            self.headers['Referer']=base_url
            print self.headers
            yield scrapy.Request(url=url, callback=self.parse_body, headers=self.headers,cookies=self.cookie)

    def parse_body(self, response):
        # date=self.date
        # 如何转换python datetime 到mongodb ？
        # response is json string
        print response.url

        js = json.loads(response.body)
        body = js['body']
        p = re.compile('"cur_city_name":"(.*?)"')

        city_name = p.findall(js['args'])[0].decode('unicode_escape')

        tree = etree.HTML(body)
        nodes = tree.xpath('//li[@class="pictext"]')
        #log.msg(len(nodes), level=log.INFO)
        for node in nodes:
            items = LianjiaItem()

            # xiaoqu_url =node.xpath('.//a[@class="flexbox post_ulog"]/@href')[0]
            # items['xiaoqu_link']=xiaoqu_url
            name = node.xpath('.//div[@class="item_list"]/div[@class="item_main"]/text()')[0]
            items['name'] = name
            desc = node.xpath('.//div[@class="item_list"]/div[@class="item_other text_cut"]/text()')[0]
            # 获取当前的城市名字
            items['city_name'] = city_name
            details = desc.split()
            if len(details) == 3:
                # 获取 小区地址 建筑时间 建筑类型

                items['location'] = details[0]
                items['building_type'] = details[1]
                items['building_date'] = details[2]
            elif len(details) == 2:
                items['location'] = details[0]
                items['building_type'] = "NA"
                items['building_date'] = details[1]
            elif len(details) == 1:
                items['location'] = details[0]
                items['building_type'] = "NA"
                items['building_date'] = 'NA'
            else:
                items['location'] = 'NA'
                items['building_type'] = "NA"
                items['building_date'] = 'NA'
            price_t = node.xpath('.//div[@class="item_list"]/div[@class="item_minor"]/span/em/text()')[0]
            p = re.findall('\d+', price_t)
            if len(p) != 0:
                price = int(price_t)
            else:
                price = '均价未知'
            # 价格信息，价格，来源，抓取时间
            price_detail = {'price': price, 'origin': 'LJ', 'crawl_date': self.crawl_date}

            price_list = []
            price_list.append(price_detail)
            price_dict = {self.price_month: price_list}
            items['price'] = price_dict
            # print 'type of items : ',type(items)
            #log.msg(items, level=log.INFO)
            yield items
