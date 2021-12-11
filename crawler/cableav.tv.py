#! /usr/bin/env python
# -*- coding:utf-8 -*-
import csv
import os
import queue
import time

import pymysql
import requests
from lxml import etree
import threading
from concurrent.futures import ThreadPoolExecutor

def mydownload(picInfo):
    url=picInfo[0]
    path=picInfo[1]
    name=picInfo[2]
    if not os.path.exists(path):
        os.makedirs(path)
    file_path = path + '/' + name

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
        with open(file_path, 'wb') as f:
            f.write(r1.content)
        return url,0
    else:
        return url,1

class ParseChapter:
    def __init__(self):
        # 链接拼接方法：1：domain+href;2:start_url+href
        self.picPath=r'D:\codehub\server\node_record\pic\cableav.tv'
        self.encoding='UTF-8'
        self.headers = {
            'Cookie': "_ga=GA1.2.1457775170.1637073040; _gid=GA1.2.214585483.1637889578; zone-cap-4330988=1",
            'user-agent':"Mozilla/5.0 (Windows NT 6.1; Win64; x64)" "AppleWebKit/537.36 (KHTML, like Gecko)" "Chrome/68.0.3440.106" "Safari/537.36"
        }
        self.db=pymysql.connect(host='localhost',
                                user='node',
                                password='954325',
                                database='db_record')
        self.cursor = self.db.cursor()
        self.listPlayList=[]
        self.listPic=[]

    def insertFile(self):
        sql="insert into t_playlist values (%s,%s,%s,%s,%s,%s,%s);"
        print('插入t_video',sql)

        # 执行SQL语句
        self.cursor.executemany(sql,self.listPlayList)
        # 提交修改
        self.db.commit()
        print('1')


    def start(self,startPage,endPage):
        existCount=0
        for i in range(startPage,endPage):
            url='https://cableav.tv/playlist/page/%s/'%(str(i))
            req=requests.get(url,headers=self.headers)

            html_tree=etree.HTML(req.text)
            listArticle=html_tree.xpath('//article')
            num=0
            for article in listArticle:
                num=num+1
                id=article.xpath('.//a[@class="blog-img"]/@data-post-id')[0]
                title=article.xpath('.//a[@class="blog-img"]/@title')[0]
                dateTime=article.xpath('./div/div[2]/div/div/div[1]/span/time[1]/@datetime')[0]
                countView=article.xpath('.//div[@class="view-count"]//text()')[0]
                countLike=article.xpath('.//div[@class="like-count"]//text()')[0]
                status=0
                picUrl=article.xpath('.//img/@data-src')[0]
                picName=os.path.basename(picUrl)
                if picName=='thumbnail.jpg':
                    picNewUrl=picUrl
                    picName=os.path.basename(picNewUrl.replace('/thumbnail.jpg','_thumbnail.jpg'))

                picLocalUrl='http://127.0.0.1:3002/pic/cableav.tv/'+picName
                node=etree.tostring(article).decode()
                node=node.replace(picUrl,picLocalUrl)
                #print('picUrl',picUrl)
                #print('node',node)
                if os.path.exists(self.picPath+'\\'+picName):
                    existCount=existCount+1
                else:
                    existCount=0
                    self.listPlayList.append((id,title,dateTime,int(countView.replace(',','')),int(countLike.replace(',','')),status,node))
                    self.listPic.append((picUrl,self.picPath,picName))
                print(i,id,title,dateTime,picUrl,picName)



            if existCount>5:

                break
            time.sleep(2)


executor = ThreadPoolExecutor(max_workers=10)

pc=ParseChapter()
pc.start(1,98)
pc.insertFile()
listPic=pc.listPic
for (url,state) in executor.map(mydownload,listPic):
    print("thread return: {}结果{}".format(url,state))