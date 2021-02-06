# -*- coding: utf-8 -*-
import scrapy
import requests
import os
import time
import csv
from concurrent.futures import ThreadPoolExecutor
import threading
from threading import Thread
import sqlite3
import json
import sys
from Queue import Queue
from concurrent.futures import ThreadPoolExecutor
import hashlib

status=0
end_num=0
db_name=''
tname=''
def update_down_info(tdata):
    global db_name,tname
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    if tdata['state']:
        tempStr='state={}'.format(tdata['state'])
    if tdata['ID']:
        whereStr='ID={}'.format(tdata['ID'])
    sqlStr='UPDATE {} SET {} WHERE {};'.format(tname,tempStr, whereStr)
    print sqlStr
    c.execute(sqlStr)
    print '更新{}下载状态为{}'.format(tdata['ID'], str(tdata['state']))
    conn.commit()
    conn.close()

def select_down_info(tdata):
    global db_name, tname
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    whereStr=' 1=1'
    if tdata['name']!='':
        whereStr =whereStr+ ' AND name={}'.format(tdata['name'])
    else:
        whereStr = whereStr + ' AND state=0'
    sqlStr='SELECT * FROM {} WHERE {} ORDER BY pageID DESC limit 20;'.format(tname,whereStr)
    print sqlStr
    c.execute(sqlStr)
    retItem=c.fetchall()
    conn.commit()
    conn.close()
    return retItem

def insert_down_info(tdata):
    global db_name, tname
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    sqlStr = 'INSERT INTO {} (pageID,state,name,folder,url) VALUES ({},{},\'{}\',\'{}\',\'{}\');'\
        .format(tname, tdata['pageID'],tdata['state'],tdata['name'],tdata['folder'],tdata['url'])
    print sqlStr
    c.execute(sqlStr)
    #retItem = c.fetchall()
    conn.commit()
    conn.close()

q = Queue()
class TPut2DB ():   # 继承父类threading.Thread
    def __init__(self):
        pass

    def PutUrl(self):
        with ThreadPoolExecutor(5) as executor:
            global end_num
            start_num=1
            end_num=5906
            for i in range(start_num, end_num):
                executor.submit(self.PutVideoUrl, i)


    def PutVideoUrl(self,i):
        time.sleep(10)
        print '线程池执行'
        pageurl = 'http://www.jimobox.com/api/v1.2/?page=' + str(i)

        result = req(pageurl)
        if not result:
            return
        jsonRet = result.json()
        for each in jsonRet['data']['items']:
            tdata={}
            tdata['name'] = str(each['id']) + '.mp4'
            ret1=select_down_info(tdata)

            if len(ret1)==0:
                tdata['state']=0

                tdata['folder'] = 'jilebox' + str(each['id']/1000)
                tdata['url']='http://www.jimobox.com/video/play/'+str(each['id'])
                insert_down_info(tdata)

        global status,end_num
        if i==end_num-1:
            status=1
            print '从网络获取下载数据完毕'


class TPushQueue ():   # 继承父类threading.Thread
    def __init__(self):
        pass

    def db2Queue(self):
        global q
        while True:
            if q.qsize()<5:
                time.sleep(10)
                tdata = {}
                tdata['name']=''
                ret1 = select_down_info(tdata)
                print '从数据库取{}条下载数据'.format(len(ret1))
                global status
                if status == 1 and len(ret1)==0:
                    print '数据库中数据读取完毕'
                    break
                for each in ret1:
                    print each[4]
                    down_info={
                        'ID':each[0],
                        'pageID': each[1],
                        'state': each[2],
                        'md5': each[3],
                        'name': each[4],
                        'folder': each[5],
                        'url': each[6]
                    }
                    q.put(down_info)

lock=threading.Lock()
class CDownload ():   # 继承父类threading.Thread
    def __init__(self,path):
        self.path=path
        self.video_md5_file='D:\视频4：md5记录及番号记录\视频md5记录集.db'.decode('utf-8')

    def set_video_md5_file(self,video_md5_file):
        self.video_md5_file=video_md5_file

    def mp4_download(self):
        while True:
            global q
            down_info=q.get()
            path=self.path+down_info['folder']+'/'
            global lock
            lock.acquire()
            try:
                if not os.path.exists(path):
                    os.makedirs(path)
            finally:
                lock.release()

            file_path=path+down_info['name']

            resp = req(down_info['url'])
            if not resp:
                continue
            state = 0
            if os.path.exists(self.video_md5_file):
                md5 = hashlib.md5()
                for chunk in resp.iter_content(chunk_size=1024):
                    if chunk:
                        md5.update(chunk)
                md5str = md5.hexdigest()
                print md5str
                state = 2
                if not IsMd5Exist(self.video_md5_file,md5str):
                    AddMD5(self.video_md5_file,md5str)
            with open(file_path, 'wb') as f:
                f.write(resp.content)
            state = 1
            tdata={
                'state':state,
                'ID':down_info['ID']
            }
            update_down_info(tdata)
            q.task_done()

class JileSpider(scrapy.Spider):
    name = 'jile1'
    allowed_domains = ['http://www.jimobox.com/']
    start_urls = ['http://www.jimobox.com/']

    def parse(self, response):
        path='D:/视频2：待归档/'.decode('utf-8')
        global db_name,tname
        db_name = 'D:\\down_info.db'
        tname = 'tVideoInfo'
        #多线程读取页面录入下载任务到数据库
        tputDB=TPut2DB()
        tputDB.PutUrl()

        #从数据库读取下载任务到队列
        pq=TPushQueue()
        t2 = Thread(target=pq.db2Queue)
        #pq.db2Queue()
        t2.start()

        #开启多线程下载
        for j in range(5):  # 新建5个线程 等待队列
            down = CDownload('D:\视频1：待入库\\'.decode('utf-8'))
            t3 = Thread(target=down.mp4_download)
            t3.setDaemon(True)
            t3.start()

        t2.join()
        q.join()


def req(url):
    i = 0
    flag = 0
    while i < 10:

        i = i + 1
        # 十次连接失败后要检测网络连接是否正常，不正常则阻塞在循环里
        if i == 10:
            netStatus = testNet()
            if netStatus == 0:
                time.sleep(5)
                i = 9

        try:
            resp = requests.get(url, verify=False, timeout=20)

            if resp.status_code == 200 :
                flag = 1
                break
        except requests.exceptions.RequestException:
            continue

    if flag == 1:
        return resp
    else:
        return False


def testNet():
    try:
        response = requests.get('https://www.baidu.com', verify=False, timeout=20)
        if response.status_code ==200:
            return 1
        if response.status_code ==404:
            return 0
    except requests.exceptions.RequestException:
        return 0
    return 1

def AddMD5(path,value):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute('INSERT INTO file_md5 (md5)VALUES (\''+value+'\');')
    print "插入一行"
    conn.commit()
    conn.close()

def IsMd5Exist(path,value):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute('SELECT id FROM file_md5 WHERE md5=\'' + value + '\';')
    ret =c.fetchall()
    conn.commit()
    conn.close()
    if len(ret)==0:
        return False
    else:
        print "MD5已经存在"
        return True
