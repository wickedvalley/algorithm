#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
爬取新闻
'''

import requests
import time
from bs4 import BeautifulSoup
import MySQLdb
import sys
from Mongdbs import *
import random

class ScrapyNews():

    #初始化相关数据
    def __init__(self,host,user,passwd,db):
        #设置页面编码
        if sys.getdefaultencoding() != 'utf-8':
            reload(sys)
            sys.setdefaultencoding('utf-8')

        #获得数据库链接
        self.db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db, charset='utf8')

        # 获取操作游标
        self.cursor =self.db.cursor()

    #获得随机的url
    def getRandUrls(self):
        data=[{'/politics':u'时政'},{'/world':u'国际'},{'/business':u'经济'},{'/social':u'社会'},
              {'/culture': u'文化'},{'/sports':u'体育'},{'/technology':u'科技'},{'/environment':u'环保'},
              {'/Travel': u'旅游'}]
        index = random.randrange(0, 9)
        for k, v in data[index].items():
            print k, v
            return k,v


    # 爬虫模块
    # 时政、时政、国际、经济、社会、文化、体育、科技、环保、旅游
    # scrapyData('https://zh.vietnamplus','/politics',"https://zh.vietnamplus.vn/politics")
    def scrapyData(self,baseUrl, mainUrl,type):
        # response=requests.post('https://zh.vietnamplus.vn/politics.vnp')
        try:
            postUrl = baseUrl + mainUrl + '.vnp';  # https://zh.vietnamplus.vn/politics.vnp
            response = requests.post(postUrl,timeout=300)
            text = response.text
            bs = BeautifulSoup(text, "html.parser")
            urls = [];  # 当前main主题下，所有的url
            totals = 0;  # 总的页数
            for item in bs.find_all(attrs={'class': 'story '}):
                newsUrl = item.a.get("href")  # 当前新闻的url，需要去重
                if mainUrl not in newsUrl:
                    urls.append(baseUrl + newsUrl)
                    #爬去对应的数据
                    self.getNewsContent(baseUrl + newsUrl, type)
        except Exception,e:
            print "获取新闻url失败"

        try:
            # 获取总页数
            for i, item in enumerate(bs.find('span', id='ctl00_mainContent_ctl00_ContentList1_pager').children):
                lens = len(item.contents);
                print "总页数:", item.contents[lens - 1].a.get_text()#获得总的分页数
                totals = item.contents[lens - 1].a.get_text()
        except Exception,e:
            print "获得分页数据失败"

        # 从所有的分页中获得所有的新闻url
        url = baseUrl + mainUrl + '/page';  # https://zh.vietnamplus.vn/politics/page
        for page in range(2, int(totals)):
            # if page == 20:
            #     return urls
            newUrl = url + str(page) + '.vnp';  # 新的时政页面
            print newsUrl
            response = requests.post(newUrl, timeout=300)
            text = response.text
            bs = BeautifulSoup(text, "html.parser")
            for item in bs.find_all(attrs={'class': 'story '}):
                newsUrl = item.a.get("href")  # 当前新闻的url，需要去重
                if mainUrl not in newsUrl:
                    urls.append(baseUrl + newsUrl)
                    print "当前页面：", page
                    print "提取的url", newsUrl
                    #爬去对应的单条新闻
                    self.getNewsContent(baseUrl+newsUrl,type)
        # return urls
        return "爬去完成"

    # 获取新闻的内容(单条url)
    def getNewsContent(self,url,type):
        try:
            response = requests.post(url, timeout=300)
            text = response.text.encode('utf8')
            print "-----------当前文本-----------",text
            bs = BeautifulSoup(text, "html.parser")
            print "标题：", bs.h1.get_text()  # 标题
            print "内容：", bs.find_all(attrs={'class': 'article-body'})[0]  # 内容
            title = bs.h1.get_text();
            content = bs.find_all(attrs={'class': 'article-body'})[0]  # 内容
        except Exception,e:
            print "获取新闻%s---失败"%url

        #判断是否抓取过
        try:
            mb = MongDBs('localhost', 27017);
            result = mb.getTitleFromMong(url);
            if result:  # 可以插入
                mb.addTitles(url)
            else:
                print "新闻：%s---已存在"%url
                return
        except Exception,e:
            print "mongDb链接异常"

        timeNow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 本地时间

        # 执行sql
        try:
            result = self.cursor.execute('insert into news(type,title,content,createTime) values("%s", "%s","%s","%s")' % \
                                    (type, title, str(content).encode('utf8').replace("\"", ""), timeNow))
            #提交事务
            self.db.commit();
            print "执行插入sql结果：", result
        except Exception,e:
            print "执行sql插入--数据已存在"


    # 从所有的新闻url中获得所有的内容
    def getNewsJob(self,urls, type):
        try:
            for url in urls:
                self.getNewsContent(url, type, self.db)
        except Exception,e:
            print "爬取数据异常";
            print e.message

    #去除重复的数据，一般不会用到
    def deleteRepeatData(self):
        try:
            rows=self.cursor.execute("delete from news where id not in( SELECT id from ((SELECT b.id from news b GROUP BY b.title) as b))")
            print "删除了%s条重复数据"%rows
        except Exception,e:
            print "去重执行失败"
        finally:
            self.cursor.close()

if __name__=='__main__':
    #获得爬虫对象
    scrapy=ScrapyNews(host='127.0.0.1', user="root", passwd="", db="ssh2");

    # #获得需要爬虫的模板
    mainUrl,type=scrapy.getRandUrls();
    #
    # #爬取内容,所有的内容
    scrapy.scrapyData('https://zh.vietnamplus.vn',mainUrl,type)

    #可以单项爬取
    #国际
    # scrapy.scrapyData('https://zh.vietnamplus.vn','/world',u'国际');

    #旅游
    # scrapy.scrapyData('https://zh.vietnamplus.vn','/Travel',u'旅游');

    #经济
    # scrapy.scrapyData('https://zh.vietnamplus.vn','/business',u'经济');

    #社会
    # scrapy.scrapyData('https://zh.vietnamplus.vn','/social',u'社会');

    #文化
    # scrapy.scrapyData('https://zh.vietnamplus.vn','/culture',u'文化');

    #体育
    # scrapy.scrapyData('https://zh.vietnamplus.vn','/sports',u'体育');

    # 科技
    # scrapy.scrapyData('https://zh.vietnamplus.vn','/technology',u'科技');

    # 环保
    # scrapy.scrapyData('https://zh.vietnamplus.vn','/environment',u'环保');

    # 时政
    # scrapy.scrapyData('https://zh.vietnamplus.vn','/politics',u'时政');
