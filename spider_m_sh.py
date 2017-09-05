# coding: utf-8
from scrapy import cmdline
import sys


def start_run(spider, city):
    city = city
    spider_name = spider
    cmd = 'scrapy crawl %s -a city=%s' % (spider_name, city)
    print cmd
    cmdline.execute(cmd.split())


start_run(sys.argv[1], sys.argv[2])
