#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import requests

class ScrapySPFYS():

    #构造初始化环境
    def __init__(self):
        #设置页面编码
        if sys.getdefaultencoding() != 'utf-8':
            reload(sys)
            sys.setdefaultencoding('utf-8')

    #爬取分页信息,商品房预售许可
    def job(self):
        data = {
            '__EVENTTARGET': 'LinkButton3',
            '__EVENTARGUMENT':None,
            '__VIEWSTATE':'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',
            '__EVENTVALIDATION':'/wEWBwKZsoTnBgLeipm1AwKM54rGBgLM9PumDwKxi96RBQKWosD8CgL7uKJnBOqHK0uSisL0BT5CoYCPJ9MRwhE=',
            'txtKeyWord':None
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Host':'fgj.wuhan.gov.cn',
            'Origin':'http://fgj.wuhan.gov.cn',
            'Referer':'http://fgj.wuhan.gov.cn/search/chaxun/kfb_spfys.aspx',
            'Proxy-Connection':'keep-alive',
            'Content-Type':'application/x-www-form-urlencoded',
            # 'Cookie':'tracker_cookie_1=True; Hm_lvt_86633ca3632934bf1675ca851ed558ed=1525671446,1525671460; ASP.NET_SessionId=rbz3vjyiqqwvdo55i4zue555; tracker_cookie_datetime_1=2018-5-7%2014%3A23%3A46; Hm_lpvt_86633ca3632934bf1675ca851ed558ed=1525674226',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate',
            'Cache-Control':'max-age=0'
        }
        response=requests.session().post("http://fgj.wuhan.gov.cn/search/chaxun/kfb_spfys.aspx",headers=headers,data=data)
        print response.text

    #获得项目概况
    def getXMGK(self):
        data = {
            '__EVENTTARGET': 'LinkButton3',
            '__EVENTARGUMENT':None,
            '__VIEWSTATE':'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',
            '__EVENTVALIDATION':'/wEWBwKZsoTnBgLeipm1AwKM54rGBgLM9PumDwKxi96RBQKWosD8CgL7uKJnBOqHK0uSisL0BT5CoYCPJ9MRwhE=',
            'txtKeyWord':None
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Host':'fgj.wuhan.gov.cn',
            'Origin':'http://fgj.wuhan.gov.cn',
            'Referer':'http://fgj.wuhan.gov.cn/search/chaxun/kfb_spfys.aspx',
            'Proxy-Connection':'keep-alive',
            'Content-Type':'application/x-www-form-urlencoded',
            # 'Cookie':'tracker_cookie_1=True; Hm_lvt_86633ca3632934bf1675ca851ed558ed=1525671446,1525671460; ASP.NET_SessionId=rbz3vjyiqqwvdo55i4zue555; tracker_cookie_datetime_1=2018-5-7%2014%3A23%3A46; Hm_lpvt_86633ca3632934bf1675ca851ed558ed=1525674226',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate',
            'Cache-Control':'max-age=0'
        }
        response=requests.session().post("http://fgj.wuhan.gov.cn/search/chaxun/kfb_spfys_view.aspx?id=2098166",headers=headers)
        print response.text

if __name__=='__main__':
    scrapy=ScrapySPFYS();
    # scrapy.job()
    scrapy.getXMGK()