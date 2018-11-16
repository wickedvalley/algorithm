#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
论坛贴吧数据爬取：
1.模拟登陆
2.爬取数据
3.存数据
'''

import sys
import time
import requests
import MySQLdb
from bs4 import BeautifulSoup

class ScrapyForms():
    # 构造初始化环境
    def __init__(self):
        # 设置页面编码
        if sys.getdefaultencoding() != 'utf-8':
            reload(sys)
            sys.setdefaultencoding('utf-8')

        #获得数据库链接
        self.db = MySQLdb.connect(host='127.0.0.1', user='root', passwd='', db='ssh2', charset='utf8')

        # 获取操作游标
        self.cursor =self.db.cursor()

    # 爬取分页信息,商品房预售许可
    def job(self):
        #原始链接
        url='https://www.hi-pda.com/forum/logging.php?action=login&sid=d2FPf8'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Host': 'www.hi-pda.com'
        }
        session=requests.session();
        response = session.get(url, headers=headers)
        cdb_sid=response.cookies['cdb_sid']#关键cookie
        print 'cdb_sid--->',cdb_sid

        #处理登陆
        url2='https://www.hi-pda.com/forum/logging.php?action=login&loginsubmit=yes&inajax=1'
        url2+='sid='+cdb_sid+'&formhash=44511a8f&referer=https%3A%2F%2Fwww.hi-pda.com%2Fforum%2Fsearch.php&loginfield=username&username=%CE%D2%CA%C7%B4%F3%CA%A6&password=08591bbe7c99e39dfa314f85d6204a00&questionid=0&answer='
        data = {
            'sid':cdb_sid,
            'formhash': '44511a8f',
            'referer':'https://www.hi-pda.com/forum/search.php',
            'loginfield':'username',
            'username':'我是大师',
            'password':'08591bbe7c99e39dfa314f85d6204a00',
            'questionid':'0',
            'answer':''
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Host': 'www.hi-pda.com',
            'Referer':'https://www.hi-pda.com/forum/logging.php?action=login&sid=d2FPf8',
            'Origin':'https://www.hi-pda.com',
            'Content-Type':'application/x-www-form-urlencoded'
        }

        response2=session.post(url2,headers=headers)

        print "cookies2:",response2.cookies


        #获取系统cookie
        '''通过request 登陆系统，获取cookie'''
        print "----获取session中的cookie----"
        cookiesList = []
        loadCookies = requests.utils.dict_from_cookiejar(session.cookies)
        for cookieName, cookieValue in loadCookies.items():
            cookies = {}
            cookies['name'] = cookieName
            cookies['value'] = cookieValue
            cookiesList.append(cookies)
        # return cookiesList

        #打开浏览器
        from selenium import webdriver
        driver = webdriver.Firefox()
        driver.get(url2)
        time.sleep(3)

        print "----1.处理cookies----"
        print "----2.获取的cookielist---",cookiesList
        for cookie in cookiesList:
            print "----cookie---",cookie
            driver.add_cookie(cookie)
            time.sleep(2)

        #重新进入首页后，可以正常访问了
        driver.get(url2)
        return


        #首页信息
        url3='https://www.hi-pda.com/forum/index.php'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Host': 'www.hi-pda.com',
            'Referer':'https://www.hi-pda.com/forum/logging.php?action=login&sid=d2FPf8',
            'Origin':'https://www.hi-pda.com',
            'Content-Type':'application/x-www-form-urlencoded'
        }
        response3 = session.post(url3, headers=headers)
        # print "-----首页信息----",str(response3.content).decode("gbk").encode("utf-8")

        #Buy & Sell 交易服务区
        url4='https://www.hi-pda.com/forum/forumdisplay.php?fid=6'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Host': 'www.hi-pda.com',
            'Referer':'https://www.hi-pda.com/forum/index.php',
            'Origin':'https://www.hi-pda.com'
        }
        response4 = session.post(url4, headers=headers)
        response4=str(response4.content).decode("gbk").encode("utf-8")



        # print "-----交易服务区信息----",response4
        bs = BeautifulSoup(response4, "html.parser")
        contents=bs.find_all('cite')
        #获得当前页的作者链接以及作者信息
        for i in contents:
            authorUrl=i.a.get("href");
            authorName=i.a.text
            if 'uid' in authorUrl and '我是大师' not in authorName:
                print "---->",authorUrl
                print "---->>",authorName

        print "---------获得作者页面的分页信息---------"
        #获得作者页面的分页信息
        contents=bs.find('div', class_='pages')
        host='https://www.hi-pda.com/forum/'
        maxPages=0;
        for i in contents.find_all('a'):
            texts=i.text
            if "下一页" not in texts:
                    texts=str(texts).replace("... ","").strip()
                    print i.get("href")
                    print "--->",texts
                    if int(texts) > maxPages:
                        maxPages=int(texts)
        print "总的分页信息是：",maxPages


        print "---开始处理分页获取作者链接---"
        self.jobs(maxPages,session,headers);
        '''
        #开启搜索模式
        url5='https://www.hi-pda.com/forum/search.php?srchuid=26171&srchfid=all&srchfrom=0&searchsubmit=yes'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Host': 'www.hi-pda.com',
            'Referer':'https://www.hi-pda.com/forum/space.php?uid=26171',
            'Origin':'https://www.hi-pda.com'
        }
        response5 = session.post(url5, headers=headers)
        response5=str(response5.content).decode("gbk").encode("utf-8")


        print "-----搜索帖子信息----"
        bs = BeautifulSoup(response5, "html.parser")
        contents=bs.find_all('tbody')
        print "执行插入数据操作："
        # 保存首页的信息
        self.saveContent(contents)

        #保存分页获得的信息
        print "分页信息"
        contents=bs.find('div', class_='pages')
        host='https://www.hi-pda.com/forum/'
        for i in contents.find_all('a'):
            texts=i.text
            if "下一页" not in texts:
                    print i.get("href")
                    newUrl=host+i.get("href")
                    pageContent=session.post(newUrl,headers=headers)
                    pageContent=str(pageContent.content).decode("gbk").encode("utf-8")#获取新的分页的具体信息
                    bs = BeautifulSoup(pageContent, "html.parser")
                    contents = bs.find_all('tbody')
                    self.saveContent(contents)
    '''
    #保存爬取的信息
    def saveContent(self,contents):
        timeNow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 本地时间
        for i in contents:
            forms=i.find('td', class_='forum').a.text #板块
            if 'Buy & Sell 交易服务区' in forms:
                subject=i.find('th', class_='subject').a.text #主题
                author=i.find('cite').a.text  #作者
                print '---->>>>',subject
                print '---->>>>', author

                try:
                    result = self.cursor.execute('insert into content(title,author,createTime) values("%s","%s","%s")'% \
                        (subject,author,timeNow))
                    # 提交事务
                    self.db.commit();
                    print "执行插入sql结果：", result
                except Exception, e:
                    print "执行sql插入--数据已存在"


    #通过板块首页的分页信息，获得所有作者信息
    def jobs(self,maxPages,session,headers):
        timeNow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 本地时间
        for index in range(2,maxPages):
            url='https://www.hi-pda.com/forum/forumdisplay.php?fid=6&page='+str(index)
            response=session.post(url,headers=headers)
            response= str(response.content).decode("gbk").encode("utf-8")
            #"-----交易服务区信息----"
            bs = BeautifulSoup(response, "html.parser")
            contents=bs.find_all('cite')
            #获得当前页的作者链接以及作者信息
            for i in contents:
                authorUrl=i.a.get("href");
                authorName=i.a.text
                if 'uid' in authorUrl and '我是大师' not in authorName:
                    print "---->",authorUrl
                    print "---->>",authorName
                    try:
                        result = self.cursor.execute('insert into authors(authorUrl,authorName,createTime) values("%s","%s","%s")'% \
                            (authorUrl,authorName,timeNow))
                        # 提交事务
                        self.db.commit();
                        print "执行插入sql结果：", result

                        uid=int(authorUrl.split("=")[1])

                        print "---进入获得内容--"
                        self.getContentByAuthorId(session,uid);
                    except Exception, e:
                        print "执行sql插入--数据已存在"

    #通过作者的id来查询作者的所有发的帖子信息
    def getContentByAuthorId(self,session,uid):
        print '开启搜索模式'
        #开启搜索模式
        url5='https://www.hi-pda.com/forum/search.php?srchuid='+str(uid)+'&srchfid=all&srchfrom=0&searchsubmit=yes'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Host': 'www.hi-pda.com',
            'Referer':'https://www.hi-pda.com/forum/space.php?uid=26171',
            'Origin':'https://www.hi-pda.com'
        }
        response5 = session.post(url5, headers=headers)
        response5=str(response5.content).decode("gbk").encode("utf-8")


        print "-----搜索帖子信息----"
        bs = BeautifulSoup(response5, "html.parser")
        contents=bs.find_all('tbody')
        print "执行插入数据操作："
        # 保存首页的信息
        self.saveContent(contents)

        #保存分页获得的信息
        print "分页信息"
        contents=bs.find('div', class_='pages')
        host='https://www.hi-pda.com/forum/'
        for i in contents.find_all('a'):
            texts=i.text
            if "下一页" not in texts:
                    print i.get("href")
                    newUrl=host+i.get("href")
                    pageContent=session.post(newUrl,headers=headers)
                    pageContent=str(pageContent.content).decode("gbk").encode("utf-8")#获取新的分页的具体信息
                    bs = BeautifulSoup(pageContent, "html.parser")
                    contents = bs.find_all('tbody')
                    self.saveContent(contents)


if __name__ == '__main__':
    scrapy = ScrapyForms();
    scrapy.job()
