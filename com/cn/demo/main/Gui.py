#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
python 界面化开发  thinker开发
'''
from tkinter import *
import threading
import time
import sys
class Gui():
    def __init__(self):

        self.count=0;

        #设置编码
        if sys.getdefaultencoding() != 'utf-8':
            reload(sys)
            sys.setdefaultencoding('utf-8')

        #设置线程标示
        self.flag = False;
        #创建窗体
        root = Tk(className="翻译工具")
        root.geometry('580x200')

        # 标签控件，显示文本和位图，展示在第一行
        Label(root, text="翻译中文：").grid(row=0, sticky=E)  # 靠右
        Label(root, text="翻译结果").grid(row=1, sticky=W)  # 第二行，靠左
        Label(root, text="任务进度").grid(row=2, sticky=W)  # 第二行，靠左

        # 显示控件
        self.titleSet = "等待需要翻译的中文"#显示标题
        self.result = "等待结果"#显示翻译结果

        self.lab1=Label(root,width=32,text="等待需要翻译的中文",justify='left')
        self.lab1.grid(row=0, column=1, padx=10, pady=10)

        self.lab2=Label(root,width=32,text="等待结果",foreground='#32CD32',justify='center')
        self.lab2.grid(row=1, column=1)

        self.lab3=Label(root,width=32,text="等待链接数据库...",foreground='#32CD32',justify='center')
        self.lab3.grid(row=2, column=1)


        label = Label(text="中英翻译工具")
        label.grid(row=0, column=2, rowspan=2, columnspan=2,
                   sticky=W + E + N + S, padx=5, pady=5)  # 合并两行，两列，居中，四周外延5个长度

        # 按钮控件
        self.button1 = Button(root, text="翻译",width=8,command=self.start)
        self.button1.grid(row=3, rowspan=2,column=0,columnspan=2,sticky=N + S,padx=5,pady=50)
        self.button2 = Button(root, text="停止",width=8,command=self.stop)
        self.button2.grid(row=3, column=2,padx=0,pady=50,sticky=N + S)

        #启动程序
        root.mainloop()

    #测试线程时候使用
    def jobDetails(self):
        return time.time()

    #线程执行的任务
    def threadJob(self):
        while (self.flag):
            self.count+=1;
            self.lab1['text'] = self.jobDetails()
            self.lab2['text']=self.jobDetails()+1
            self.lab3['text'] = str(self.count)+"%"
            time.sleep(1)
            print time.time()

    def start(self):
        print "开启线程start"
        self.button1['state']=DISABLED
        self.flag=True
        t = threading.Thread(target=self.threadJob, args=(), name='thread-refresh')
        t.setDaemon(True)
        t.start()

    #停止线程
    def stop(self):
        self.flag=False
        self.button1['state'] = NORMAL


if __name__=='__main__':
    gui=Gui();

