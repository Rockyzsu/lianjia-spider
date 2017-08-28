# coding: utf-8
import hashlib

import time


def mayiproxy():
    my_app_key = "235817354"
    app_secret = "9dab67c52899767b69d31b0c8ef06ebd"
    mayi_url = 's3.proxy.mayidaili.com'
    mayi_port = '8123'

    # 蚂蚁代理服务器地址
    #mayi_proxy = {'http': 'http://{}:{}'.format(mayi_url, mayi_port)}
    mayi_proxy = 'http://{}:{}'.format(mayi_url, mayi_port)
    timesp = '{}'.format(time.strftime("%Y-%m-%d %H:%M:%S"))
    codes = app_secret + 'app_key' + my_app_key + 'timestamp' + timesp + app_secret
    sign = hashlib.md5(codes.encode('utf-8')).hexdigest().upper()

    # 拼接一个用来获得蚂蚁代理服务器的「准入」的 header (Python 的 concatenate '+' 比 join 效率高)
    authHeader = 'MYH-AUTH-MD5 sign=' + sign + '&app_key=' + my_app_key + '&timestamp=' + timesp

    return mayi_proxy,authHeader