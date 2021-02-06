#! /usr/bin/env python
import re
import time
from concurrent.futures import ThreadPoolExecutor

import scrapy

from jileboxPic.spiders.db.DownInfo import DownInfo
from jileboxPic.spiders.globalValue import *
from jileboxPic.spiders.req import req


class jimobox_Video():   # 继承父类threading.Thread
    def __init__(self,):
        pass

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
        domains = 'http://www.3333box.com/'
        #film_list_api = 'http://www.jimobox.com/api/v1.4/?page=' + str(i)
        video_list_api = '{}api/v1.2/?page={}'.format(domains,str(i))

        result = req(video_list_api)
        if not result:
            return
        jsonRet = result.json()
        for each in jsonRet['data']['items']:
            tdata = {}
            tdata['name'] = str(each['id']) + '.mp4'
            # TODO:使用数据库
            db = get_global_value('db')
            ret1 = db.select_down_info(tdata)

            if len(ret1) == 0:
                tdata['state'] = 0
                tdata['pageID']=each['id']
                tdata['folder'] = 'jilebox' + str(each['id'] // 1000)
                tdata['url'] = '{}video/play/{}'.format(domains,str(each['id']))
                tdata['key']=''
                # TODO:使用数据库
                db.insert_down_info(tdata)
