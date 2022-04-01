#! /usr/bin/env python
import re
import time
from concurrent.futures import ThreadPoolExecutor

import scrapy

from jileboxPic.spiders.db.DownInfo import DownInfo
from jileboxPic.spiders.globalValue import *
from jileboxPic.spiders.req import req


class jimobox_tsVideo():   # 继承父类threading.Thread
    def __init__(self):
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
            res_page_film_show = req(film_show_page_url)
            if not res_page_film_show:
                continue
            selector1 = scrapy.Selector(res_page_film_show)
            films = selector1.xpath('//*[@class="xuanji"]/a/@href').extract()
            # 长度太长的影片会有多个播放页
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
                # 5.获取m3u8文件
                m3u8 = req(m3u8_uri)
                # 没有key.key
                pattern1 = re.compile(r",(.*?)#")
                tslist = pattern1.findall(re.sub('\n', '', m3u8.text))
                index = 0
                for ts in tslist:

                    index += 1
                    tdata = {}
                    tdata['name'] = '{}_{}_{}.ts'.format(file_view_id, len(tslist), index)
                    # TODO:使用数据库
                    db = get_global_value('db')
                    ret3 = db.select_down_info(tdata)

                    if len(ret3) == 0:
                        tdata['pageID'] = each['id']
                        tdata['state'] = 0
                        tdata['folder'] = '{}/{}_{}'.format(i // 10, each['id'], each['desk'])
                        tdata['url'] = re.sub('master.m3u8', ts, m3u8_uri)
                        tdata['key'] = ''

                        db.insert_down_info(tdata)
