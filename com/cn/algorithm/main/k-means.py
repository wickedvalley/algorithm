#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
from numpy import *
import random
import matplotlib.pyplot as plt

#计算两个样本之间的欧式距离
#参数是矩阵
def calDistance(vec1,vec2):
    vec1=array(vec1);#转为数组
    vec2 = array(vec2);
    return sqrt(sum(pow(vec1-vec2,2)));

#随机选取初始质心
def getInitCentroid(dataSet,k):
    m,n=shape(dataSet);
    centroid=zeros((k,n));#初始化k个质心
    for i in range(k):
        index=random.uniform(0,len(dataSet));
        centroid[i,:]=dataSet[int(index),:];
    return mat(centroid);

#核心算法
def kmeans(dataSet,k):
    m,n=shape(dataSet);
    clusterAssment=mat(zeros((m,1)))#初始化簇m行，1列，第一列为元素所属的簇  说明：簇也就是所属的类，类就是我们常说的标签
    centroid=getInitCentroid(dataSet,k)#获得初始质心
    isEnd=True;
    while isEnd:
        isEnd=False;
        for i in range(len(dataSet)):#对于每一个样本
            minDistance=100000;
            minindex=-1;
            for j in range(k):#寻找离质心最近的簇
                distance=calDistance(dataSet[i,:],centroid[j,:])
                if distance<minDistance:
                    minDistance=distance;
                    minindex=j#寻找到了离质心最近的簇
            if clusterAssment[i,0] != minindex:#若簇有变化，更新簇
                isEnd=True;
                clusterAssment[i,0]=minindex

        for n in range(k):#更新每个质心
            test1=clusterAssment[:, 0].A==n#获得与质心类型相同的簇
            test2=nonzero(test1);
            test3=test2[0];#获得与质心类型相同簇元素的下标
            test4=dataSet[test3]
            centroid[n,:]=mean(test4,axis=0);#相同的簇，计算平均值即为新的质心，axis=0为对列求平均值
    return centroid,clusterAssment

#加载数据
def loadData(filePath):
    dataSet=[];
    with open(filePath) as f:
        for line in f.readlines():
            lines=line.split("\t");
            dataSet.append([float(lines[0]),float(lines[1])]);
    return mat(dataSet)


#画图
def showCluster(dataSet, k, centroids, clusterAssment):
    numSamples, dim = dataSet.shape
    if dim != 2:
        print("Sorry! I can not draw because the dimension of your data is not 2!")
        return 1

    #颜色
    mark = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']
    if k > len(mark):
        print("Sorry! Your k is too large! please contact Zouxy")
        return 1

    #画样本
    for i in range(numSamples):
        markIndex = int(clusterAssment[i, 0])  # 每个样本所属族群
        plt.plot(dataSet[i, 0], dataSet[i, 1], mark[markIndex])
    mark = ['Dr', 'Db', 'Dg', 'Dk', '^b', '+b', 'sb', 'db', '<b', 'pb']

    #画质心
    for i in range(k):
        plt.plot(centroids[i, 0], centroids[i, 1], mark[i], markersize=6)
    plt.show()

if __name__=='__main__':
    dataPath=os.getcwd()+"\\train.txt";
    dataSet=loadData(dataPath);#加载数据
    centroid, clusterAssment=kmeans(dataSet,2)#knn算法，返回质心以及簇
    showCluster(dataSet,2,centroid,clusterAssment);#作图

