#!/usr/bin/python
# -*- coding: UTF-8 -*-


import time

with open("D:\\password.txt",'w') as f:
    for i in range(1,10):
        f.writelines([str(i)+"\n"])

f.close()