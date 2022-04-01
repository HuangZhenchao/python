#! /usr/bin/env python
import re
import time
from concurrent.futures import ThreadPoolExecutor

import scrapy

from jileboxPic.spiders.db.DownInfo import DownInfo
from jileboxPic.spiders.globalValue import *
from jileboxPic.spiders.req import req


class jimobox_photo():   # 继承父类threading.Thread
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
        pic_list_api = '{}api/v1.1/?page={}'.format(domains,str(i))

        ret1 = req(pic_list_api)
        if not ret1:
            return
        retjson1 = ret1.json()
        for each in retjson1['data']['items']:
            photo_page_url = '{}photo/{}'.format(domains,each['id'])
            ret2 = req(photo_page_url)
            if not ret2:
                continue

            selector = scrapy.Selector(ret2)
            pic_urls = selector.xpath('//*[@id="baidu_image_holder"]/a/img/@src').extract()
            index = 0
            for pic_url in pic_urls:
                index += 1
                tdata = {}
                tdata['name'] = '{}_{}_{}.jpg'.format(each['id'], len(pic_urls), index)
                # TODO:使用数据库
                db = get_global_value('db')
                retdata = db.select_down_info(tdata)

                if len(retdata) == 0:
                    tdata['state'] = 0
                    tdata['pageID'] = each['id']
                    tdata['folder'] = 'jile_photo/' + str(each['id'] // 1000)
                    tdata['url'] = pic_url
                    tdata['key']=''
                    db.insert_down_info(tdata)
