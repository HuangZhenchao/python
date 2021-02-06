# -*- coding: utf-8 -*-
import scrapy
import requests
import os
import time
import csv
from concurrent.futures import ThreadPoolExecutor
import sys

class JileSpider(scrapy.Spider):
    name = 'html2text'
    allowed_domains = ['http://www.xixibox.com/']
    start_urls = ['http://www.xixibox.com/']

    def parse(self, response):
        domains='http://www.xixibox.com/'
        moduleArr=['video/']
        for module in moduleArr:
            with ThreadPoolExecutor(3) as executor:
                for collectionOrder in range(683,685):#750
                    path='D:/Spider Resource/jilebox.com/'+module+str(collectionOrder)
                    for id in range(collectionOrder*1000,collectionOrder*1000+1000):
                        array={
                                'domains':domains,
                                'module':module,
                                'path':path,
                                'collectionOrder':collectionOrder,
                                'id':id,
                        }
                        executor.submit(mydownload, array)
                        #mydownload(array)
                        time.sleep(5)


def mydownload(array):
    domains=array['domains']
    module=array['module']
    path=array['path']
    collectionOrder=array['collectionOrder']
    id=array['id']
    print id
    if not os.path.exists(path):
        os.makedirs(path)
    url = domains+module+'play/'+str(id)
    name = str(id)+'.mp4'
    #下载视频
    downStatus=downVideo(url, path, name)
    stu=[id, downStatus['statusCode']]
    write2csv(path+'/video_'+str(collectionOrder)+'.csv', stu)
    time.sleep(5)

def downVideo(url, path, name):
    downStatus={}
    path = path + '/' + name
    i = 0
    flag = 0
    while i < 10:
        i = i + 1
        try:
            r1 = requests.get(url, verify=False, timeout=20)
            if r1.status_code == 200:
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