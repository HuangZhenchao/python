# -*- coding: utf-8 -*-
import scrapy
import requests
import os
import re
import chardet
import time
import csv
from concurrent.futures import ThreadPoolExecutor
import sys
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class JileSpider(scrapy.Spider):
    name = 'jile'
    allowed_domains = ['http://www.mmonly.cc/']
    start_urls = ['http://www.mmonly.cc/']

    def parse(self, response):
        domains='http://www.mmonly.cc/'
        moduleArr=['mmtp/swmn/']
        for module in moduleArr:
            with ThreadPoolExecutor(5) as executor:
                # 750
                for collectionOrder in range(0,8):#860
                    for id in range(collectionOrder*10+1,collectionOrder*10+11):
                        array={
                                'domains':domains,
                                'module':module,
                                'path':'D:/Spider Resource/mmonly.cc/'+module+str(collectionOrder),
                                'collectionOrder':collectionOrder,
                                'id':id,
                        }
                        executor.submit(mydownload, array)
                        #mydownload(array)
                        time.sleep(5)


def mydownload(array):
    domains=array['domains']
    module=array['module']
    path = array['path']
    collectionOrder=array['collectionOrder']
    id=array['id']
    if not os.path.exists(path):
        os.makedirs(path)

    url = domains + module + 'list_11_'+str(id)+'.html'
    print id
    i = 0
    flag=0
    while i < 10:

        i = i + 1
        #十次连接失败后要检测网络连接是否正常，不正常则阻塞在循环里
        if i==10:
            netStatus=testNet()
            if netStatus==0:
                time.sleep(5)
                i=9

        try:
            respListpage = requests.get(url, verify=False, timeout=20)

            #print resp_listpage.apparent_encoding
            respListpage.encoding='GB2312'

            with open('D:/test.html', "ab") as f:
                f.write(respListpage.content)
            if respListpage.status_code == 200:
                flag = 1
                break
        except requests.exceptions.RequestException:
            continue

    if flag == 1:
        selector = scrapy.Selector(respListpage)
        links = selector.xpath('//*[@class="title"]/span/a')

        for index, link in enumerate(links):
            sContentPageTitle = link.xpath('text()').extract()[0]
            #print repr(sContentPageTitle)
            sContentPageUrl=link.xpath('@href').extract()[0]
            #novelid=re.findall('/book/(.*)', sContentPageUrl)[0]
            print sContentPageTitle,sContentPageUrl

            #path = path + '/' + sContentPageTitle+'.txt'
            iContentPartNum=0
            bTurnPage=True
            while bTurnPage:
                iContentPartNum=iContentPartNum+1
                if iContentPartNum==1:
                    sContentPartUrl=sContentPageUrl
                else:
                    sPartNumReplaceStr='_'+str(iContentPartNum)+'.html'
                    sContentPartUrl=sContentPageUrl.replace('.html',sPartNumReplaceStr)
                j=0
                while j < 10:
                    j = j + 1
                    if j == 10:
                        netStatus = testNet()
                        if netStatus == 0:
                            time.sleep(5)
                            j = 9
                    try:
                        resp_contentpage = requests.get(sContentPartUrl, verify=False, timeout=20)

                        # result.encoding = 'utf-8'
                        selector1 = scrapy.Selector(resp_contentpage)
                        sPicUrl = selector1.xpath('//*[@id="big-pic"]/p[@align="center"]/a/img/@src').extract()[0]
                        print sPicUrl
                        resp_pic = requests.get(sPicUrl, verify=False, timeout=20)
                        filedir=path+'/'+sContentPageTitle+str(iContentPartNum)+'.jpg'
                        print filedir
                        with open(filedir, "ab") as f:
                            f.write(resp_pic.content)

                        sNextPageUrl = selector1.xpath('//*[@id="nl"]/a/@href').extract()[0].encode('utf-8')
                        if sNextPageUrl=='##':
                            bTurnPage = False
                        break
                    except requests.exceptions.RequestException:
                        continue


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