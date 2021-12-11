#! /usr/bin/env python
# -*- coding:utf-8 -*-
import os

import requests
import html2text
from lxml import etree

class ParseChapter:
    def __init__(self,start_url):
        # 链接拼接方法：1：domain+href;2:start_url+href
        rule_list={'http://www.xinyushuwu.com/':['//*[@class="ml_list"]//li/a',2,'//*[@id="articlecontent"]'],}

        self.start_url=start_url
        self.domain='http://www.xinyushuwu.com/'

        self.rule=rule_list[self.domain]
        self.encoding=''
        self.headers = {
            'user-agent':"Mozilla/5.0 (Windows NT 6.1; Win64; x64)" "AppleWebKit/537.36 (KHTML, like Gecko)" "Chrome/68.0.3440.106" "Safari/537.36"
        }
    def setEncoding(self,req):
        encoding=''
        if req.encoding == 'ISO-8859-1':
            encodings = requests.utils.get_encodings_from_content(req.text)
            if encodings:
                encoding = encodings[0]
            else:
                encoding = req.apparent_encoding
            if encoding=='gb2312':
                encoding='gbk'
        else:
            encoding=req.encoding
        self.encoding=encoding
        req.encoding=encoding

    def start(self):
        req=requests.get(self.start_url,headers=self.headers)

        self.setEncoding(req)
        print(self.rule)
        html_tree=etree.HTML(req.text)
        title=html_tree.xpath('//title/text()')[0]
        links=html_tree.xpath(self.rule[0])
        print(links)
        index=0
        text=""
        for link in links:
            index+=1
            link_text=link.xpath('./text()')[0]
            print(link_text)
            link_href=link.xpath('./@href')[0]
            text=text+self.parseChapterPage(link_href)
        file_dir='D:\\OneNoteTempFile'
        # if not os.path.exists(file_dir):
        #     os.mkdir(file_dir)
        file_name=title+'.txt'
        file_path=file_dir+'\\'+file_name
        with open(file_path,'a',encoding='utf-8') as f:
             f.write(text)
        # print(text)

    def parseChapterPage(self,link_href):
        if self.rule[1]==1:
            chapterUrl=self.domain+link_href
        if self.rule[1]==2:
            chapterUrl=self.start_url+link_href
        print(chapterUrl,self.start_url+chapterUrl)
        req=requests.get(chapterUrl,headers=self.headers)
        req.encoding=self.encoding
        # print(req.text)
        html_tree=etree.HTML(req.text)
        div=html_tree.xpath(self.rule[2])[0]
        h=html2text.HTML2Text()
        h.ignore_links=True
        text=h.handle(etree.tostring(div, pretty_print=True).decode())
        return text


pc=ParseChapter('http://www.xinyushuwu.com/4/4823/')
pc.start()