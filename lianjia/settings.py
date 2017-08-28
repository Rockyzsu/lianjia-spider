# -*- coding: utf-8 -*-

# Scrapy settings for lianjia project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'lianjia'

SPIDER_MODULES = ['lianjia.spiders']
NEWSPIDER_MODULE = 'lianjia.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'lianjia (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 2

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
'''
DEFAULT_REQUEST_HEADERS = {
    'Host': 'm.lianjia.com',
    'Cache-Control':'no-cache',
    'Connection':'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Pragma': 'no-cache',
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
    # 'User-Agent': 'UCWEB/2.0 (Linux; U; Adr 2.3; zh-CN; MI-ONEPlus) U2/1.0.0 UCBrowser/8.6.0.199 U2/1.0.0 Mobile',
    'X-Requested-With': 'XMLHttpRequest',
    'Cookie': 'lianjia_uuid=bd5695e2-e708-40ed-a422-bd7735eb0913; UM_distinctid=15dca9b5775ed-0270ab60593b6d-791238-1fa400-15dca9b5776535; _jzqy=1.1502342765.1503554600.1.jzqsr=baidu|jzqct=%E9%93%BE%E5%AE%B6.-; lj-ss=040f750f334914ad3f62a65590f5df64; lj-api=eb773d00ac95736a80cb663e13368872; sample_traffic_test=guide_card; select_nation=1; _jzqckmp=1; _smt_uid=5993d85d.c78ffd9; _jzqa=1.1287000182441332700.1502861406.1503645894.1503648405.6; _jzqc=1; _jzqx=1.1503558036.1503648405.2.jzqsr=sz%2Elianjia%2Ecom|jzqct=/ershoufang/.jzqsr=captcha%2Elianjia%2Ecom|jzqct=/; select_city=440100; CNZZDATA1253491255=2028382610-1503555874-%7C1503645723; _ga=GA1.2.154142580.1502861407; _gid=GA1.2.332017260.1503554602; _gat=1; _gat_past=1; _gat_new=1; _gat_global=1; _gat_new_global=1; CNZZDATA1254525948=292510229-1503555399-%7C1503650077; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1502861405,1503378424,1503554600; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1503650375; lianjia_ssid=0293b735-bdd1-41dc-b933-052e24413aec'
}
'''

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'lianjia.middlewares.LianjiaSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'lianjia.middlewares.MyCustomDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'lianjia.pipelines.LianjiaPipeline': 300,
}
MONGODB_SERVER = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB = 'house'
MONGODB_COLLECTION = 'dummy4'

REDISDB_SERVER = 'localhost'
REDISDB_PORT = 6379
REDISDB_DB = 'test'
REDISDB_COLLECTION = 'houseinfo'
# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
    'lianjia.middlewares.ProxyMiddleware': 100,
}