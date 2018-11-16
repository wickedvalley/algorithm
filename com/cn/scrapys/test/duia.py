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

        self.session = requests.session();


    # 对啊网视频地址获取
    def job(self):

        url='http://live.duia.com/video/get/videoUrl'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
            'Host': 'live.duia.com',
            'Origin':'http://live.duia.com',
            'Referer':'http://live.duia.com/video/play/1310/50807',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With':'XMLHttpRequest',
            # 'Cookie':'NTKF_T2D_CLIENTID=guest65D3B6B7-8E98-531B-5116-BA8463F5D05B; nTalk_CACHE_DATA={uid:kf_9751_ISME9754_guest65D3B6B7-8E98-53,tid:1527842628597910}; Hm_lvt_7807b581bd39ca93734ed246857f588e=1527842632; SESSION=7795a9bb-da66-497c-bb8d-fb982167e963; MEIQIA_EXTRA_TRACK_ID=15PPDWM6mHEXyw72i4MU8JqrnVF; Hm_lpvt_7807b581bd39ca93734ed246857f588e=1527842661'
        }
        data={
            'lectureId':'50807',
            'params':'rY1TJdK5KbI2FrOzzE3XXt4kutYpODce+cLy3BzB0TFwY8rOiRBYNRnPV96gd1O92E+0mpFgTGZLeP54Oak/vE4PT6GWxGXh7Nj7798/ZshIJhvKu+Z+x2W3ZJHezfdXJSBJmnz6zIo/tz5PvUEdCsUSNVkalJTf1xfAhIDc1VbI77LbEo9bxlTTGE05kypV9mJdBTAvnsS59/Rhr2fbzA=='
        }
        response=self.session.post(url=url,headers=headers,data=data)
        print response.text


if __name__ == '__main__':
    scrapy = Scrapy();
    scrapy.job()
