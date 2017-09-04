# coding: utf-8
from scrapy import cmdline
import sys
def start_run(spider,city):
    city_sh=city
    spider_name=spider
    cmd='scrapy crawl %s -a city=%s' %(spider_name,city_sh)
    print cmd
    cmdline.execute(cmd.split())

print "Args : ",sys.argv[1],sys.argv[2]
start_run(sys.argv[1],sys.argv[2])