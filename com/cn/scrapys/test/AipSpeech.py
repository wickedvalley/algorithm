#!/usr/bin/python
# -*- coding: UTF-8 -*-
from aip import AipSpeech
import pymongo

class ApiSpeech:
    def __init__(self):
        APP_ID = '11664983'
        API_KEY = 'sIYRpWFTTO6k4DtGjFHKmsEo'
        SECRET_KEY = 'hvv6OEiK5Tm9KhNs5vM8m9FlBpaWIBoG '

        self.client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    # 读取文件
    def get_file_content(selef,filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    # 识别本地文件
    def requestApi(self):
        return self.client.asr(self.get_file_content('D:\\data\\2.wav'), 'wav', 16000, {
            'dev_pid': 1536,
        })

if __name__ == '__main__':
    print "start world"
    api = ApiSpeech();
    result = api.requestApi();
    print result
    print "hello world"