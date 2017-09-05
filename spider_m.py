# coding: utf-8
import json

import subprocess
from scrapy import cmdline
import sys
def start_run(spider):
    fp=open('city_name.txt','r')
    city_dict=json.load(fp)
    std_fp=open('spider.log','a')
    err_fp=open('spider_err.log','a')
    for city_key,city_name in city_dict.items():
        if city_key == "sh" or city_key =="su":
            continue
        spider_name=spider
        cmd='scrapy crawl %s -a city=%s' %(spider_name,city_key)
        print cmd
        #cmdline.execute(cmd.split())
        subprocess.Popen(cmd,stdout=std_fp,stderr=err_fp,shell=True)
start_run(sys.argv[1])

