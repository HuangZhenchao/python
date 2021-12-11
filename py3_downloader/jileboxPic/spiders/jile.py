# -*- coding: utf-8 -*-
import scrapy
import requests
import os
import time
import csv
import hashlib
from concurrent.futures import ThreadPoolExecutor
import sys
import sqlite3
class JileSpider(scrapy.Spider):
    name = 'jile'
    allowed_domains = ['http://www.jimobox.com/']
    start_urls = ['http://www.jimobox.com/']

    def parse(self, response):
        domains='http://www.jimobox.com/'#http://www.xixibox.com/
        moduleArr=['video/']
        for module in moduleArr:
            with ThreadPoolExecutor(5) as executor:
                # 750
                for i in range(1, 2):
                    path='D:/视频1：待入库/'.decode('utf-8')
                    pageurl = 'http://www.jimobox.com/api/v1.2/?page=' + str(i)
                    result = requests.get(pageurl, headers={'Connection': 'close'}, verify=False, allow_redirects=False,
                                          timeout=50)
                    jsonRet=result.json()
                    for each in jsonRet['data']['items']:

                        collectionOrder=int(each['id'])/1000
                        array={
                                'domains':domains,
                                'module':module,
                                'path':path+str(collectionOrder)+'/',
                                'collectionOrder':collectionOrder,
                                'id':each['id'],
                        }
                        executor.submit(mydownload, array)
                        #mydownload(array)
                        time.sleep(5)


def mydownload(array):
    domains=array['domains']
    module=array['module']
    path=array['path']
    #collectionOrder=array['collectionOrder']
    id=array['id']
    print id
    if not os.path.exists(path):
        os.makedirs(path)
    url = domains+module+'play/'+str(id)

    #下载视频
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
        name = '##@jilebox%video&'+str(id) + '$##.mp4'
        print name
        file_path = path + '/' + name
        with open(file_path, 'wb') as f:
            f.write(r1.content)


'''
def downVideo(url, path, name):
    downStatus={}
    i = 0
    flag = 0
    while i < 10:
        i = i + 1
        try:
            r1 = requests.get(url, stream=True, verify=False, timeout=20)
            if r1.status_code == 200:
                flag = 1
                break
        except requests.exceptions.RequestException:
            continue

    if flag == 1:
        total_size = int(r1.headers['Content-Length'])
        if os.path.exists(path):
            temp_size = os.path.getsize(path)  # 本地已经下载的文件大小
        else:
            temp_size = 0  # 显示一下下载了多少
        path = path +'/'+ name
        i = 0
        downStatus['statusCode']=2
        downStatus['message']='下载未完成'
        while i<10:
            i = i + 1          
            if total_size==temp_size:
                downStatus['statusCode']=1
                downStatus['message']='下载完成'
                break
            try:
                # 核心部分，这个是请求下载时，从本地文件已经下载过的后面下载
                headers = {'Range': 'bytes=%d-' % temp_size}
                # 重新请求网址，加入新的请求头的
                video = requests.get(url, stream=True, verify=False, headers=headers, timeout=20)
            except requests.exceptions.RequestException:
                continue
            with open(path, "ab") as f:
                for chunk in video.iter_content(chunk_size=1024):
                    if chunk: 
                        temp_size += len(chunk)
                    f.write(chunk)
                    f.flush()

        downStatus['total_size']=total_size
        downStatus['done']=temp_size
        return downStatus
    if flag == 0:
        downStatus['statusCode']=0
        downStatus['message']='访问资源地址失败'
        downStatus['total_size']=0
        downStatus['done']=0
        return downStatus
'''

def write2csv(filedir, stu):
    # write file
    # 打开文件，追加a
    out = open(filedir, 'ab')
    # 设定写入模式
    csv_write = csv.writer(out, dialect='excel')
    csv_write.writerow(stu)
    out.close()