#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
操作mongdb，主要用于防止爬取重复数据
'''
from pymongo import MongoClient
class MongDBs:
    def __init__(self,serverName,porn):
        self.client = MongoClient('localhost', 27017)#获得链接
        self.db=self.client.news#获得db连接
        self.collection = self.db.news#从链接中获得集合

    #插入数据
    def addTitles(self,title):
        self.collection.insert({'title': title})

    #从数据库里查数据
    def getTitleFromMong(self,title):
        flag = self.collection.find_one({'title': title})
        if flag==None:
            return True#不存在该数据，可以插入
        return False#存在该数据

    #获得所有的数据
    def printAll(self):
        for item in self.collection.find():
            print item

    #关闭mongdb
    def close(self):
        try:
            self.client.close();
        except Exception,e:
            print e.message

if __name__=='__main__':
    mb=MongDBs('localhost', 27017);
    title='张三';
    result=mb.getTitleFromMong(title);
    if result:#可以插入
        mb.addTitles(title)
    mb.printAll()
