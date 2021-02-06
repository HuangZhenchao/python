import queue
from threading import Thread

import scrapy

from .Downloader import CDownload
from .PushQueue import CPushQueue
from .UrlSpider import UrlSpider
from .globalValue import *

status=0
end_num=0

class JileSpider(scrapy.Spider):
    name = 'jile1'
    allowed_domains = ['http://avtt37.com/']
    start_urls = ['http://avtt37.com/']

    def parse(self, response):
        #首先获取操作系统信息，设置数据库文件位置以及下载文件保存位置
        #db_path_DownInfo
        save_path='D:\视频1：待入库/'
        q = queue.Queue()
        set_global_value('queue',q)
        set_global_value('CrawlDone',0)

        #多线程读取页面录入下载任务到数据库
        tUrlSpider=UrlSpider()
        tUrlSpider.PutUrl()

        #从数据库读取下载任务到队列
        pq=CPushQueue()
        t2 = Thread(target=pq.db2Queue)
        #pq.db2Queue()
        t2.start()

        #开启多线程下载
        for j in range(5):  # 新建5个线程 等待队列
            t3 = Thread(target=TDown(save_path))
            t3.setDaemon(True)
            t3.start()

        t2.join()
        q.join()


def TDown(save_path):
    while True:
        q=get_global_value('queue')
        down_info=q.get()
        down = CDownload(save_path)
        down.download(down_info)
        q.task_done()