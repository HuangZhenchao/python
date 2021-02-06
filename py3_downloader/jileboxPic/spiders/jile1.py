import queue
from threading import Thread
import sys
import scrapy

from jileboxPic.spiders.UrlSpider.avtt37_TsVideo import avtt37_TsVideo
from jileboxPic.spiders.UrlSpider.jimobox_TsVideo import jimobox_tsVideo
from jileboxPic.spiders.UrlSpider.jimobox_Video import jimobox_Video
from jileboxPic.spiders.UrlSpider.jimobox_photo import jimobox_photo

from .Downloader import CDownload
from .PushQueue import CPushQueue
from .db.DownInfo import DownInfo
from .globalValue import *

status=0
end_num=0

class JileSpider(scrapy.Spider):
    name = 'jile1'
    allowed_domains = ['http://avtt37.com/','http://www.3333box.com/']
    start_urls = ['http://avtt37.com/','http://www.3333box.com/']

    def parse(self, response):
        #首先获取操作系统信息，设置数据库文件位置以及下载文件保存位置
        #db_path_DownInfo

        file_save_path='E:\\test/'
        db_name='D:\\DownInfo.db'
        FileInfo_tname = 'tTsVideoInfo_avtt'
        md5Info_tname = ''
        start_page=1
        end_page=1        #645
        '''
        file_save_path = sys.argv[1]
        db_name =  sys.argv[2]
        FileInfo_tname =  sys.argv[3]
        md5Info_tname = ''
        start_page =  int(sys.argv[4])
        end_page =  int(sys.argv[5])
        '''
        q = queue.Queue()

        set_global_value('queue',q)
        set_global_value('CrawlDone',0)
        set_global_value('file_save_path',file_save_path)
        set_global_value('db_name', db_name)

        set_global_value('FileInfo_tname', FileInfo_tname)
        set_global_value('md5Info_tname', md5Info_tname)


        #多线程读取页面录入下载任务到数据库
        if FileInfo_tname == 'tTsVideoInfo':
            tUrlSpider=jimobox_tsVideo()
            #tUrlSpider = avtt37_TsVideo()
        if FileInfo_tname == 'tTsVideoInfo_avtt':
            tUrlSpider=avtt37_TsVideo()
        if FileInfo_tname == 'tVideoInfo':
            set_global_value('md5Info_tname', 'video_md5')
            tUrlSpider = jimobox_Video()
        if FileInfo_tname == 'tPicInfo':
            set_global_value('md5Info_tname', 'pic_md5')
            tUrlSpider = jimobox_photo()

        db = DownInfo()
        set_global_value('db', db)

        tUrlSpider.GetUrlStart(start_page,end_page)

        #从数据库读取下载任务到队列
        pq=CPushQueue()
        t2 = Thread(target=pq.db2Queue)
        #pq.db2Queue()
        t2.start()

        #开启多线程下载
        for j in range(5):  # 新建5个线程 等待队列
            t3 = Thread(target=TDown)
            t3.setDaemon(True)
            t3.start()

        t2.join()
        q.join()


def TDown():
    while True:
        q=get_global_value('queue')
        down_info=q.get()
        down = CDownload()
        down.download(down_info)
        q.task_done()