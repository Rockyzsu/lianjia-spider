# -*-coding=utf-8-*-
import requests
from lxml import etree
def get_city_link():
    headers={'Host':'m.lianjia.com','User-Agent':'UCWEB/2.0 (Linux; U; Adr 2.3; zh-CN; MI-ONEPlus) U2/1.0.0 UCBrowser/8.6.0.199 U2/1.0.0 Mobile'}
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
