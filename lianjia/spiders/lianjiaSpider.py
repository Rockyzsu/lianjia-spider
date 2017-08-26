# coding: utf-8
import json
import re

import datetime
from lxml import etree
import scrapy
from lianjia.items import LianjiaItem
class Lianjia_Spider(scrapy.Spider):
    name='lianjia'
    allowed_domains=['m.lianjia.com']
    start_urls=['https://m.lianjia.com/hz/xiaoqu/pg1/?_t=1',
                ]
    date=datetime.datetime.now().strftime('%Y-%m-%d')
    '''
    def start_requests(self):
        url='https://m.lianjia.com/hz/xiaoqu/pg1/?_t=1'
    '''
    def __init__(self):
        self.date=datetime.datetime.now().strftime('%Y-%m-%d')
        self.header= {
            'Host': 'm.lianjia.com',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Pragma': 'no-cache',
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
            'User-Agent': 'UCWEB/2.0 (Linux; U; Adr 2.3; zh-CN; MI-ONEPlus) U2/1.0.0 UCBrowser/8.6.0.199 U2/1.0.0 Mobile',
            'X-Requested-With': 'XMLHttpRequest',
            'Cookie': 'lianjia_uuid=bd5695e2-e708-40ed-a422-bd7735eb0913; UM_distinctid=15dca9b5775ed-0270ab60593b6d-791238-1fa400-15dca9b5776535; _jzqy=1.1502342765.1503554600.1.jzqsr=baidu|jzqct=%E9%93%BE%E5%AE%B6.-; lj-ss=040f750f334914ad3f62a65590f5df64; lj-api=eb773d00ac95736a80cb663e13368872; sample_traffic_test=guide_card; select_nation=1; _jzqckmp=1; _smt_uid=5993d85d.c78ffd9; _jzqa=1.1287000182441332700.1502861406.1503645894.1503648405.6; _jzqc=1; _jzqx=1.1503558036.1503648405.2.jzqsr=sz%2Elianjia%2Ecom|jzqct=/ershoufang/.jzqsr=captcha%2Elianjia%2Ecom|jzqct=/; select_city=440100; CNZZDATA1253491255=2028382610-1503555874-%7C1503645723; _ga=GA1.2.154142580.1502861407; _gid=GA1.2.332017260.1503554602; _gat=1; _gat_past=1; _gat_new=1; _gat_global=1; _gat_new_global=1; CNZZDATA1254525948=292510229-1503555399-%7C1503650077; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1502861405,1503378424,1503554600; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1503650375; lianjia_ssid=0293b735-bdd1-41dc-b933-052e24413aec'
        }

    def getTotalCount(self,url):


    def parse(self, response):


        for i in range(1,5):
            url='https://m.lianjia.com/sz/xiaoqu/pg%d/?_t=1'  %i
            yield scrapy.Request(url=url,headers=self.header,callback=self.parse_body)

    def parse_body(self,response):
        #date = datetime.datetime.now().strftime('%Y-%m-%d')
        #temp=date
        date=self.date
        # response is json string
        js = json.loads(response.body)
        body = js['body']
        #city_name=js['args']['cur_city_name']
        p = re.compile('"cur_city_name":"(.*?)"')
        city_name = p.findall(js['args'])[0].decode('unicode_escape')
        tree = etree.HTML(body)
        nodes = tree.xpath('//li[@class="pictext"]')
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
            items['price'] = int(price)
            items['scrapy_date'] = date
            items['origin']='链家'
            print 'type of items : ',type(items)
            yield items