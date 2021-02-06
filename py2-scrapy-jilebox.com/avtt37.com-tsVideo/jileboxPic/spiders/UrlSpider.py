#! /usr/bin/env python
import re
import time
from concurrent.futures import ThreadPoolExecutor

import scrapy

from jileboxPic.spiders.db.tTsVideo_avtt import tTsVideo_avtt
from .globalValue import *
from .req import req


class UrlSpider ():   # 继承父类threading.Thread
    def __init__(self):
        pass

    def PutUrl(self):
        with ThreadPoolExecutor(5) as executor:
            global end_num
            start_num=70
            end_num=70
            for i in range(start_num, end_num):
                executor.submit(self.Spider_jimobox_TsVideoUrl, i)
            #time.sleep(50)
            set_global_value('CrawlDone',1)
            print('从网络获取下载数据完毕')

    def Spider_jimobox_TsVideoUrl(self,i):
        time.sleep(10)
        print('线程池执行')
        #1.分页从URL获取影片列表
        domains='http://avtt37.com/'
        module='shipin3/toupaizipai/'   #shipin3/koujiaoxilie/  shipin3/yewaichezhen/   shipin3/wanghongzhubo/
        list_page_url='{}{}list_{}.html'.format(domains,module,str(i))
        res_list_page = req(list_page_url)
        if not res_list_page:
            return
        #2.从分页列表页解析视频地址
        selector = scrapy.Selector(res_list_page)
        video_show_urls = selector.xpath('//*[@class="channel_pic"]/ul/li/a/@href').extract()
        for video_show_url in video_show_urls:
            video_id = re.findall('/(\d*).html', video_show_url)[0]
            video_play_url = '{}{}play_{}.html'.format(domains,module,video_id)
            res_play=req(video_play_url)
            if not res_play:
                continue
            # m3u8地址被编码，解码后获取m3u8地址
            video_title=re.findall(r"<title>(.*?)在线播放 - AV天堂网</title>", res_play.content)[0]
            print(video_title.decode('utf-8'))
            m3u8_url_coded = re.findall(r"playVideo\('#player', '(.*?)', {", res_play.text)[0]
            m3u8_url = decode_m3u8_url(m3u8_url_coded)

            #5.获取并解析m3u8文件
            res_m3u8=req(m3u8_url)
            # 事先查看m3u8文件，只是一些信息，不是包含ts文件列表的m3u8
            # 替换地址，继续获取
            if not res_m3u8:
                continue
            #print m3u8_url
            substr2=re.findall('\n(.*?)index.m3u8',res_m3u8.text)[0]+'index.m3u8'
            print(m3u8_url)
            m3u8_url_final=re.sub('index.m3u8',substr2,m3u8_url)
            print(substr2)
            print(m3u8_url_final)
            res_m3u8_final=req(m3u8_url_final)
            if not res_m3u8_final:
                continue

            #avtt里的m3u8是有key.key的
            #获取key文件
            key_url=re.sub('index.m3u8', 'key.key', m3u8_url_final)
            print(key_url)
            res_key=req(key_url)
            if not res_key:
                continue

            key=res_key.text
            print(key)
            #获取到ts文件列表
            pattern1 = re.compile(r",(.*?)#")
            tslist = pattern1.findall(re.sub('\n', '', res_m3u8_final.text))
            index=0
            for ts in tslist:

                index+=1
                tdata = {}
                tdata['name'] = '{}_{}_{}.ts'.format(video_id, len(tslist), index)
                # TODO:使用数据库
                ret3 = tTsVideo_avtt.select_down_info(tdata)

                if len(ret3) == 0:
                    tdata['pageID'] = video_id
                    tdata['state'] = 0

                    tdata['folder'] = '{}{}/{}_{}'.format(module,i/10,video_id, video_title)
                    print(tdata)
                    tdata['url'] = re.sub('index.m3u8', ts, m3u8_url_final)
                    tdata['key'] = key
                    # TODO:使用数据库
                    tTsVideo_avtt.insert_down_info(tdata)




def decode_m3u8_url(md5codestring):
    import base64
    import hashlib
    string=base64.b64decode(md5codestring)
    key='just a test'
    b = hashlib.md5()
    b.update(key.encode(encoding='utf-8'))
    key=b.hexdigest()
    # len = key.length
    # print len
    code=''
    for i in range(0,len(string)):
        k=i%len(key)
        code+=chr(ord(string[i])^ord(key[k]))
    videourl=base64.b64decode(code)
    return videourl