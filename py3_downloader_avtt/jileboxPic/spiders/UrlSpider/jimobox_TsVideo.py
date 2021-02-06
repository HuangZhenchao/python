#! /usr/bin/env python
import re
import time
import sqlite3
from concurrent.futures import ThreadPoolExecutor

import scrapy

from jileboxPic.spiders.db.DownInfo import DownInfo
from jileboxPic.spiders.globalValue import *
from jileboxPic.spiders.req import req


class jimobox_tsVideo():   # 继承父类threading.Thread
    def __init__(self):
        self.db_name = 'D:/DownInfo.db'

        self.ts_table_name = 'ts_task_3333box'
        self.m3u8_table_name = 'm3u8_task_3333box'

    def GetUrlStart(self,start_page=1,end_page=1):
        with ThreadPoolExecutor(5) as executor:
            for i in range(start_page, end_page):
                executor.submit(self.SiteParser, i)
            #time.sleep(50)
        set_global_value('CrawlDone',1)
        print('从网络获取下载数据完毕')

    def SiteParser(self,i):
        time.sleep(10)
        print('线程池执行')
        #1.分页从URL获取影片列表
        domains='http://www.3333box.com/'
        film_list_api = '{}api/v1.4/?page={}'.format(domains,str(i))
        ret1 = req(film_list_api)
        if not ret1:
            return
        retjson1 = ret1.json()
        # 10个一页
        for each in retjson1['data']['items']:
            # 2.进入film的showPage页，从HTML中提取播放页的ID
            film_show_page_url = '{}film/show/{}'.format(domains,str(each['id']))
            #TODO:此处要进行数据库查询：页面是否已提取资源URL

            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            sqlStr = 'SELECT * FROM {} WHERE DetailPageUrl=\'{}\';'.format(self.m3u8_table_name, film_show_page_url)
            print(sqlStr)
            c.execute(sqlStr)
            retItem = c.fetchall()
            conn.commit()
            conn.close()
            b_URL_Exist = False
            if len(retItem)>0:
                b_URL_Exist=True
            if b_URL_Exist:
                print('页面{}已爬取'.format(film_show_page_url))
                continue
            res_page_film_show = req(film_show_page_url)
            if not res_page_film_show:
                continue
            selector1 = scrapy.Selector(res_page_film_show)
            films = selector1.xpath('//*[@class="xuanji"]/a/@href').extract()
            # 长度太长的影片会有多个播放页

            #TODO:连接数据库，把一个或者视频作为一个m3u8任务。提交时要把两个表的INSERT作为事务提交
            conn = sqlite3.connect(self.db_name)
            index = 0

            for film_url in films:
                file_view_id = re.findall('/film/view/(.*)', film_url)[0]
                # 3.获取播放页的ID后构建获取m3u8视频的API
                m3u8_api = '{}api/v1.4/view/{}'.format(domains,file_view_id)
                ret2 = req(m3u8_api)
                if not ret2:
                    continue
                print(ret2)
                retjson2 = ret2.json()

                # 4.获取真正的m3u8地址
                m3u8_uri = retjson2['data']['uri']
                print(m3u8_uri)
                # 5.获取m3u8文件
                m3u8 = req(m3u8_uri)
                # 没有key.key
                pattern1 = re.compile(r",(.*?)#")
                tslist = pattern1.findall(re.sub('\n', '', m3u8.text))
                index1=0
                for ts in tslist:
                    index += 1
                    index1+=1
                    child_task_name = '{}_{}_{}.ts'.format(each['id'], len(tslist), index1)
                    ts_uri = re.sub('master.m3u8', ts, m3u8_uri)

                    # TODO:使用数据库

                    sqlStr = 'INSERT INTO {} (DetailPageUrl,ts_name,ts_uri) ' \
                             'VALUES (\'{}\',\'{}\',\'{}\');'.format(self.ts_table_name,film_show_page_url, child_task_name, ts_uri,)
                    print(sqlStr)
                    conn.execute(sqlStr)
            key = ''
            sqlStr = 'INSERT INTO {} (DetailPageUrl,ResourceType,ResourceUrl,ResourceDetail,ChildTaskTotal,key) ' \
                         'VALUES (\'{}\',\'{}\',\'{}\',\'{}\',{},\'{}\');'.format(self.m3u8_table_name,film_show_page_url, 'm3u8', m3u8_uri,each['desk'],index,key)
            # ContentPageUrl,ResourceType,ResourceUrl,ResourceDetail,TaskStart,ChildTaskTotal,ChildTaskTotalList,ChildTaskDone,ChildTaskDoneList,TaskDone
            print(sqlStr)
            conn.execute(sqlStr)
            conn.commit()
            conn.close()
            print('执行了没有？')


