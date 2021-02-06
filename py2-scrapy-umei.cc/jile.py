# -*- coding: utf-8 -*-
import scrapy
import requests
import os
import time
import csv
import threading
import sys

class JileSpider(scrapy.Spider):
    name = 'jile'
    allowed_domains = ['http://www.jlhz001.com/']
    start_urls = ['http://www.jlhz001.com/']

    def parse(self, response):
        for num in range(687523, 690000):
            id = num
            purl = 'http://www.jlhz001.com/video/' + str(id)
            # 创建新线程
            thread1 = myThread(id, purl)
            # 开启线程
            thread1.start()
            thread1.join()
            time.sleep(1)


class myThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, id, url):
        threading.Thread.__init__(self)
        self.id = id
        self.url = url

    def writetocsv(self,filedir, id, detail, url,index):
        # write file
        # 打开文件，追加a
        out = open(filedir, 'ab')
        # 设定写入模式
        csv_write = csv.writer(out, dialect='excel')
        stul=[id, detail, url,index]
        csv_write.writerow(stul)
        out.close()

    def run(self):
        i = 0
        while i < 10:
            try:
                result = requests.get(self.url, headers={'Connection': 'close'}, verify=False, allow_redirects=False, timeout=5)
                i = i + 1
                if result.status_code == 200:
                    selector2 = scrapy.Selector(result)
                    pic_url = selector2.xpath('//*[@id="baidu_image_holder"]/video/@src').extract()
                    index=0
                    for each in pic_url:
                        index=index+1
                        print '正在下载第' + str(self.id) + '组第'+str(index)+'张图片，图片地址:' + str(each)
                        try:
                            r1 = requests.get(each, stream=True, verify=False, timeout=10)
                            if result.status_code == 200:
                                total_size = int(r1.headers['Content-Length'])
                                name = str(self.id) + "_" + each.split("/")[5]
                                path = 'F:\\' + ('[娱乐]视频').decode('utf-8') + '\jilePic69\\'

                                if not os.path.exists(path):
                                    os.makedirs(path)
                                path = path + name
                                if os.path.exists(path):
                                    temp_size = os.path.getsize(path)  # 本地已经下载的文件大小
                                else:
                                    temp_size = 0  # 显示一下下载了多少
                                print(temp_size)
                                print(total_size)
                                # 核心部分，这个是请求下载时，从本地文件已经下载过的后面下载
                                headers = {'Range': 'bytes=%d-' % temp_size}
                                # 重新请求网址，加入新的请求头的
                                video = requests.get(each, stream=True, verify=False, headers=headers)

                                with open(path, "ab") as f:
                                    for chunk in video.iter_content(chunk_size=1024):
                                        if chunk: temp_size += len(chunk)
                                        f.write(chunk)
                                        f.flush()  ###这是下载实现进度显示####
                                        done = int(50 * temp_size / total_size)
                                        sys.stdout.write("\r[%s%s] %d%%" % ('█' * done, ' ' * (50 - done), 100 * temp_size / total_size))
                                        sys.stdout.flush()
                                print()
                            if result.status_code == 404:
                                print '第' + str(self.id) + '组第'+str(index)+'张图片不存在'
                                # write file
                                detail = 'Each RequestException'
                                self.writetocsv('F:/jilePicEachRequestException_69.csv', self.id, detail, each, index)
                        except requests.exceptions.RequestException:
                            print '第' + str(self.id) + '组第'+str(index)+'张图片获取异常'
                            # write file
                            detail = 'Each RequestException'
                            self.writetocsv('F:/jilePicEachRequestException_69.csv', self.id, detail, each, index)
                            continue

                    break
                if result.status_code == 404:
                    # write file
                    print '第' + str(self.id) + '组图片不存在'
                    detail='Page404'
                    self.writetocsv('F:/jilePicPage404_69.csv', self.id, detail, '', '')
                    break
            except requests.exceptions.RequestException:
                print '获取页面异常'
                # write file
                detail = 'PageRequestException'
                self.writetocsv('F:/jilePicPageRequestException_69.csv', self.id, detail, '', '')
                continue


