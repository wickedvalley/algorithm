#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import numpy as np
import matplotlib.pyplot as plt

def loadDataSet(filePath):
    dataMat=[];
    labelMat=[];
    fr=open(filePath);
    for line in fr.readlines():
        lineArr=line.split("\t");
        dataMat.append([1.0,float(lineArr[0]), float(lineArr[1])]);
        labelMat.append(int(lineArr[2]));
    return dataMat,labelMat;

def sigmod(z):
    return 1/(1+np.exp(-z));

def gradAscent(dataMat,label):
    dataMat=np.mat(dataMat);
    label=np.mat(label).transpose();
    m,n=np.shape(dataMat);
    alpha=0.034;
    maxCycle=5000;
    weight=np.ones((n,1));
    for i in range(maxCycle):
        out=sigmod(dataMat*weight);
        error=label-out;
        weight=weight+alpha*dataMat.transpose()*error;
    return weight

def classfy(x,weights):
    label=sigmod(x*weights);
    if label>0.5:
        return 1;
    else:
        return 0;


def plotBestFit(weights,filePath):

    #导入数据

    dataMat, labelMat = loadDataSet(filePath)

    #创建数组

    dataArr = np.array(dataMat)

    #获取数组行数

    n = np.shape(dataArr)[0]

    #初始化坐标

    xcord1 = []; ycord1 = []

    xcord2 = []; ycord2 = []

    #遍历每一行数据

    for i in range(n):

        #如果对应的类别标签对应数值1，就添加到xcord1，ycord1中

        if int(labelMat[i]) == 1:

            xcord1.append(dataArr[i,1]); ycord1.append(dataArr[i,2])

        #如果对应的类别标签对应数值0，就添加到xcord2，ycord2中

        else:

            xcord2.append(dataArr[i,1]); ycord2.append(dataArr[i,2])

    #创建空图

    fig = plt.figure()

    #添加subplot，三种数据都画在一张图上

    ax = fig.add_subplot(111)

    #1类用红色标识，marker='s'形状为正方形

    ax.scatter(xcord1, ycord1, s=30, c='red', marker='s')

    #0类用绿色标识，弄认marker='o'为圆形

    ax.scatter(xcord2, ycord2, s=30, c='green')

    #设置x取值，arange支持浮点型

    x = np.arange(-3.0, 3.0, 0.1)

    #配计算y的值

    y = (-weights[0]-weights[1]*x)/weights[2]

    #画拟合直线

    ax.plot(x, y)

    #贴坐标表头

    plt.xlabel('X1'); plt.ylabel('X2')

    #显示结果

    plt.show()


if __name__=='__main__':
    filePath=os.getcwd()+"\\train.txt"
    dataArr, labelMat = loadDataSet(filePath)
    weights = gradAscent(dataArr, labelMat)
    print (weights)
    plotBestFit(weights.getA(),filePath)
    param =[1,-0.017612,14.053064];
    label=classfy(param,weights);
    print label