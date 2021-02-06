#! /usr/bin/env python
import time

from jileboxPic.spiders.db.tTsVideo_avtt import tTsVideo_avtt
from .globalValue import *

class CPushQueue ():   # 继承父类threading.Thread
    def __init__(self):
        pass

    def db2Queue(self):
        q=get_global_value('queue')
        while True:
            if q.qsize()<5:
                time.sleep(10)
                tdata = {}
                tdata['name']=''
                #TODO:使用数据库
                ret1 = tTsVideo_avtt.select_down_info(tdata)
                print('从数据库取{}条下载数据'.format(len(ret1)))

                CrawlDone=get_global_value('CrawlDone')
                if CrawlDone == 1 and len(ret1)==0:
                    print('数据库中数据读取完毕')
                    break
                for each in ret1:
                    #print each[4]
                    down_info={
                        'ID':each[0],
                        'pageID': each[1],
                        'state': each[2],
                        'md5': each[3],
                        'name': each[4],
                        'folder': each[5],
                        'url': each[6],
                        'key':each[7]
                    }
                    q.put(down_info)