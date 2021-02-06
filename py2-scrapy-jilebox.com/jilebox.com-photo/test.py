#!/usr/bin/python
# coding=utf-8
import threading
import time
import requests
import os

def downVideo(url, path, name):
    downStatus={}
    path = path + '\\' + name
    i = 0
    flag = 0
    while i < 10:
        i = i + 1
        try:
            r1 = requests.get(url, verify=False, timeout=20)
            if r1.status_code == 200 or r1.status_code == 302:
                flag = 1
                break
        except requests.exceptions.RequestException:
            continue

    if flag == 1:
        with open(path, "ab") as f:
            f.write(r1.content)
        #downStatus['total_size'] = total_size
        #downStatus['done'] = temp_size
        downStatus['statusCode'] = 1
        downStatus['message'] = '下载完成'
        return downStatus

    if flag == 0:
        downStatus['statusCode'] = 0
        downStatus['message'] = '访问资源地址失败'
        return downStatus

path='D:\Spider Resource\\avtt37.com\shipin1\guochanzipai\\15'
if not os.path.exists(path):
    os.makedirs(path)
url = 'http://jj.ima18999.com/playapi/93301'
name = '93301.mp4'
#下载视频
downStatus=downVideo(url, path, name)