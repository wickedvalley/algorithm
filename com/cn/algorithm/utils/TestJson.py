#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import csv
import json
import jieba
import nltk
from sklearn import cross_validation


class TextMain():

    def __init__(self):
        if sys.getdefaultencoding() != 'utf-8':
            reload(sys)
            sys.setdefaultencoding('utf-8')
        self.labelList=[];#训练数据集标签
        self.dataSet=[];#训练数据集

        self.trainCount=0;#训练数据数量
        self.labelCount=0;#训练数据


        #用户测试
        self.testSet=[];
        self.testLable=[];
        self.testDataCount=0;#测试数据数量
        self.testlabelCount=0;#测试数据

    #训练
    def trainSet(self):
        filePath=os.getcwd()+"\\train.json"
        file = open(filePath,'r')
        for line in file.readlines():
            self.trainCount+=1;
            dic = json.loads(line)
            id=dic['id']
            s=str(dic['content']).decode('utf-8').encode("utf8")
            s=s.replace("<title>","").replace("</title>","").replace("<html>","")\
                .replace("</html>","").replace("</html>","").replace("<p>","")\
                .replace("</p>","").replace("<body>","").replace("</body>","")\
                .replace('/<img.+(width=\"?\d*\"?).+>/i',"")\
                .replace("<font>","").replace("</font>","").replace("<strong>","").replace("</strong>","").replace("(<img.*?>)","");

            print "------id:%s---content:%s"%(id,s)
            self.dataSet.append(s)
            if self.trainCount == 10000:
                break;

    # 训练标签
    def readCsv(self):
        filePath = os.getcwd() + "\\train.csv";
        file=csv.reader(open(filePath,'r'))
        for line in file:
            if 'id' in line:
                continue
            self.labelCount+=1;
            id=line[0]
            label=line[1];
            self.labelList.append(label);
            if self.labelCount == 10000:
                break;
            # print (id,label)


    #--------------------测试数据---------------------
    #测试数据
    def testDatas(self):
        filePath=os.getcwd()+"\\train.json"
        file = open(filePath,'r')
        for line in file.readlines():
            self.testDataCount+=1;
            if self.testDataCount > 10000:
                dic = json.loads(line)
                id=dic['id']
                s=str(dic['content']).decode('utf-8').encode("utf8")
                s=s.replace("<title>","").replace("</title>","").replace("<html>","")\
                    .replace("</html>","").replace("</html>","").replace("<p>","")\
                    .replace("</p>","").replace("<body>","").replace("</body>","")\
                    .replace('/<img.+(width=\"?\d*\"?).+>/i',"")\
                    .replace("<font>","").replace("</font>","").replace("<strong>","").replace("</strong>","").replace("(<img.*?>)","");

                print "------id:%s---content:%s"%(id,s)
                self.testSet.append(s)
            if self.testDataCount==11000:
                break
        return self.testSet

    #测试数据，标签
    def testDataLabel(self):
        filePath = os.getcwd() + "\\train.csv";
        file=csv.reader(open(filePath,'r'))
        for line in file:
            if 'id' in line:
                continue
            self.testlabelCount+=1;
            if self.testlabelCount > 10000:
                id=line[0]
                label=line[1];
                self.testLable.append(label);
                print "---标签--",(id,label)
            if self.testlabelCount ==11000:
                break
        return self.testLable

if __name__=='__main__':

    textMain=TextMain();

    #csv文件，读取标签
    # filePath = os.getcwd() + "\\train.csv"
    # textMain.readCsv(filePath)
    #
    # #json文件，读取内容
    # filePath=os.getcwd()+"train.json";
    # textMain.trainSet()
    #
    # dataSet=textMain.dataSet
    # labels=textMain.labelList

    testData=textMain.testDatas();
    testLabel=textMain.testDataLabel();
    print len(testData),len(testLabel)




