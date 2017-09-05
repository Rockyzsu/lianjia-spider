# coding: utf-8
import json
import re, time
import datetime
from lxml import etree
import scrapy
from lianjia.items import LianjiaItem

class Lianjia_Spider_Mobile(scrapy.Spider):
    name = 'lianjia_m'
    allowed_domains = ['m.lianjia.com']

    def __init__(self,city=None,*args, **kwargs):
        super(Lianjia_Spider_Mobile,self).__init__(*args, **kwargs)
        self.city = city

        self.start_urls=['https://m.lianjia.com/%s/xiaoqu/pg1/?_t=1' %self.city]

        self.crawl_date = datetime.datetime.now().strftime('%Y-%m-%d')

        with open('citys_count.txt', 'r') as fp_city_count:
            citys_count = json.load(fp_city_count)

        self.xiaoqu_count = citys_count[self.city]
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
        #self.cookie={'_jzqa': '1.206544328628398600.1503881786.1503881786.1503881786.1', 'lj-ss': '1e5c8b6bb356c2aabadd162c97341948', 'lianjia_ssid': '9410766c-34bd-4115-a879-5b11375f9924', 'Hm_lpvt_9152f8221cb6243a53c83b956842be8a': '1504102362', '_ga': 'GA1.2.885541457.1503837305', 'ubta': '3154866423.1593962235.1503840667336.1503845425552.1503845426709.19', 'CNZZDATA1254525948': '1758800946-1503835682-%7C1504098054', '_smt_uid': '59a36a39.a7e32ae', 'select_nation': '1', '_gid': 'GA1.2.726828377.1504101487', 'CNZZDATA1253491255': '597282999-1503832971-%7C1504101820', 'gr_user_id': '9895cc06-d162-4985-b42c-0cc98cdee98f', '__xsptplus696': '696.2.1503843548.1503845425.16%234%7C%7C%7C%7C%7C%23%237HfP43631brEPPGQ4VLVKcfdTX7U_iad%23', 'lianjia_uuid': 'ca5a64ec-9cbe-4f31-8499-f06c3ea622da', 'UM_distinctid': '15e23b039a53a7-0b6a06eff463b1-5c153d17-1fa400-15e23b039a68d1', 'select_city': '441300', 'Hm_lvt_9152f8221cb6243a53c83b956842be8a': '1503837305,1503881786,1504101487'}
        self.cookie={'lianjia_uuid': 'ca5a64ec-9cbe-4f31-8499-f06c3ea622da', '_gat_new': '1', '_jzqa': '1.206544328628398600.1503881786.1503881786.1503881786.1', 'lj-ss': '1e5c8b6bb356c2aabadd162c97341948', 'Hm_lpvt_9152f8221cb6243a53c83b956842be8a': '1504542040', '_gat': '1', '_smt_uid': '59a36a39.a7e32ae', 'CNZZDATA1253491255': '597282999-1503832971-%7C1504541193', 'gr_user_id': '9895cc06-d162-4985-b42c-0cc98cdee98f', 'ubt_load_interval_b': '1504537420276', '_gat_past': '1', '_ga': 'GA1.2.885541457.1503837305', 'CNZZDATA1254525948': '1758800946-1503835682-%7C1504541662', 'select_nation': '1', 'UM_distinctid': '15e23b039a53a7-0b6a06eff463b1-5c153d17-1fa400-15e23b039a68d1', 'select_city': '440300', '_gat_new_global': '1', 'lianjia_ssid': 'c76950fe-ad1d-43b6-9dbd-825dc40fc561', 'ubtd': '4', 'ubta': '3154866423.1593962235.1503840667336.1504537420288.1504537421470.26', 'ubtc': '3154866423.1593962235.1504537421471.54A8769FA2903B4254B688736A67011F', '_gid': 'GA1.2.893652375.1504537910', '__xsptplus696': '696.5.1504537420.1504537420.1%234%7C%7C%7C%7C%7C%23%23Dyu9Xh4KKNw0aqvAFjtibtSfVngPI3dg%23', '_gat_global': '1', 'Hm_lvt_9152f8221cb6243a53c83b956842be8a': '1503881786,1504101487,1504454486,1504537910'}

        self.price_month = '2017-07'


    def parse(self, response):
        pages = (self.xiaoqu_count + 25) / 25

        for i in range(1, pages+1):
            base_url='https://m.lianjia.com/%s/xiaoqu/pg%d/' %(self.city,i)
            url = base_url+'?_t=1'
            self.headers['Referer']=base_url
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
