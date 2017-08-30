# -*-coding=utf-8-*-
import json
import re,codecs

import requests,os
from lxml import etree

def fetch_cookie():
    '''
    将从浏览器上Copy来的cookie字符串转化为Scrapy能使用的Dict
    :return:
    '''
    with open('lianjia_cookie.txt', 'r') as fp:
        cookie = fp.read().strip()
    itemDict = {}
    items = cookie.split(';')
    for item in items:
        key = item.split('=')[0].replace(' ', '')
        value = item.split('=')[1]
        itemDict[key] = value
    return itemDict

def get_city_link():
    cookie=str(fetch_cookie())

    headers={'Host':'m.lianjia.com','User-Agent':'UCWEB/2.0 (Linux; U; Adr 2.3; zh-CN; MI-ONEPlus) U2/1.0.0 UCBrowser/8.6.0.199 U2/1.0.0 Mobile',
             'Cookie':cookie}

    url='https://m.lianjia.com/city/'
    r=requests.get(url=url,headers=headers)
    contnet=r.text
    #print contnet
    tree=etree.HTML(contnet)
    t1=tree.xpath('//ul[@class="item_lists"]')[1]
    city_list=[]
    for city in t1:
        link= city.xpath('.//a/@href')[0]
        if link=='/sh/':
            continue
        if link=='/su/':
            continue
        if link=='/xsbn/':
            continue
        city_list.append('https://m.lianjia.com'+link)

    return city_list

def getXiaoquCount():
        cookie = str(fetch_cookie())

        headers = {            'Host': 'm.lianjia.com',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Pragma': 'no-cache',
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
            'User-Agent': 'UCWEB/2.0 (Linux; U; Adr 2.3; zh-CN; MI-ONEPlus) U2/1.0.0 UCBrowser/8.6.0.199 U2/1.0.0 Mobile',
            'X-Requested-With': 'XMLHttpRequest',
            #'Proxy-Authorization': self.authHeader
               'Cookie': cookie}
        city_count={}
        city_link=get_city_link()
        for city in city_link:
            print city
            city_code=city.split('/')[3]
            request_url = city+'xiaoqu/pg1/?_t=1'
            r=requests.get(url=request_url,headers=headers)
            xiaoqu_count = re.findall(r'\\"total\\":(\d+)}', r.text)[0]
            city_count[city_code]=int(xiaoqu_count)
        print city_count
        city_str=json.dumps(city_count)
        '''
        print city_str
        with open('city_count.txt','w') as fp:
            fp.write(city_str)
        return city_count
        '''
#getXiaoquCount()
print type(fetch_cookie())


