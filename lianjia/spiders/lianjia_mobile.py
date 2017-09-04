# coding: utf-8
import json
import re, time
import datetime
from lxml import etree
import scrapy
from lianjia.items import LianjiaItem

class Lianjia_Spider(scrapy.Spider):
    name = 'lianjia_m'
    allowed_domains = ['m.lianjia.com']

    def __init__(self,city=None,*args, **kwargs):
        super(Lianjia_Spider).__init__(,self,*args, **kwargs)
        self.city = city

        self.start_urls=['https://m.lianjia.com/%s/xiaoqu/pg1/?_t=1' %self.city]

        self.crawl_date = datetime.date.today()

        self.headers = {
            'Host': 'm.lianjia.com',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.8',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        self.cookie={'_jzqa': '1.206544328628398600.1503881786.1503881786.1503881786.1', 'lj-ss': '1e5c8b6bb356c2aabadd162c97341948', 'lianjia_ssid': '9410766c-34bd-4115-a879-5b11375f9924', 'Hm_lpvt_9152f8221cb6243a53c83b956842be8a': '1504102362', '_ga': 'GA1.2.885541457.1503837305', 'ubta': '3154866423.1593962235.1503840667336.1503845425552.1503845426709.19', 'CNZZDATA1254525948': '1758800946-1503835682-%7C1504098054', '_smt_uid': '59a36a39.a7e32ae', 'select_nation': '1', '_gid': 'GA1.2.726828377.1504101487', 'CNZZDATA1253491255': '597282999-1503832971-%7C1504101820', 'gr_user_id': '9895cc06-d162-4985-b42c-0cc98cdee98f', '__xsptplus696': '696.2.1503843548.1503845425.16%234%7C%7C%7C%7C%7C%23%237HfP43631brEPPGQ4VLVKcfdTX7U_iad%23', 'lianjia_uuid': 'ca5a64ec-9cbe-4f31-8499-f06c3ea622da', 'UM_distinctid': '15e23b039a53a7-0b6a06eff463b1-5c153d17-1fa400-15e23b039a68d1', 'select_city': '441300', 'Hm_lvt_9152f8221cb6243a53c83b956842be8a': '1503837305,1503881786,1504101487'}
        self.price_month = '2017-07'

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
        pages = (4833 + 25) / 25

        for i in range(1, pages+1):
            base_url='https://m.lianjia.com/%s/xiaoqu/pg%d/' %(self.city,i)
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
            items['price']=price_dict
            yield items
