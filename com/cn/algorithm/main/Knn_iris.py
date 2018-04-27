#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
knn算法
'''
import os
import numpy as py
import operator

#加载数据
def loadData(filePath):
    dataSet=[];
    lable=[];
    with open(filePath) as f:
        for line in f.readlines():
            lines=line.split(",");
            dataSet.append([float(lines[0]),float(lines[1]),float(lines[2]),float(lines[3])]);#获得每一行数据的前4列
            lable.append(lines[4]);#当前数据的标签
    return py.array(dataSet),lable #dataSet转为数组

#knn算法
def knn(trainSet,label,testSet,k):
    distance=(trainSet-testSet)**2;#求差的平方和---注意：数组可以做加减，此处均为数组
    distanceLine=distance.sum(axis=1);#对数组的每一行求和，axis=1为对行求和，axis=0为对每列求和
    finalDistance=distanceLine**0.5;#对和开方
    sortedIndex=finalDistance.argsort();#获得排序后原始下角标
    index=sortedIndex[:k];#获得距离较小的前k个下角标
    labelCount={};#字典  key为标签，value为标签出现的次数
    for i in index:
        tempLabel=label[i];
        labelCount[tempLabel]=labelCount.get(tempLabel,0)+1;
    sortedCount=sorted(labelCount.items(),key=operator.itemgetter(1),reverse=True);#operator.itemgetter(1)意思是按照value值排序，即按照欧氏距离排序
    return sortedCount[0][0];

#预测正确率
def predict(trainSet,trainLabel,testSet,k):
    total=len(testSet);#测试样本总数
    trueCount=0;
    for i in range(len(testSet)):
        label=knn(trainSet,trainLabel,testSet[i],k);
        if label in testLabel[i]:
            trueCount=trueCount+1;
    return float(trueCount)/float(total)

if __name__=='__main__':
    trainPath=os.getcwd()+"\\iris_train.txt";
    testPath=os.getcwd()+"\\iris_test.txt";
    trainSet,trainLabel=loadData(trainPath);#训练数据以及标签
    testSet, testLabel = loadData(testPath);#测试数据以及标签
    print predict(trainSet,trainLabel,testSet,3)
