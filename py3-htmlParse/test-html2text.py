#! /usr/bin/env python  
# -*- coding:utf-8 -*-
import os

import requests
import html2text
from lxml import etree

class ParseChapter:
    def __init__(self):
        self.base_Url='http://www.guoxue123.cn/zhibu/0101/01xs/'
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
        req=requests.get(self.base_Url+'index.htm',headers=self.headers)
        self.setEncoding(req)
        html_tree=etree.HTML(req.text)
        div=html_tree.xpath('/html/body/div[2]/table')[0]
        links=div.xpath('.//a')
        index=0
        for link in links:
            index+=1
            link_text=link.xpath('./text()')[0]
            print(link_text)
            link_href=link.xpath('./@href')[0]
            text=self.parseChapterPage(link_href)
            file_dir='D:\\OneNoteTempFile\\新书'
            if not os.path.exists(file_dir):
                os.mkdir(file_dir)
            file_name=str(index)+link_text+'.txt'
            file_path=file_dir+'\\'+file_name
            with open(file_path,'a',encoding='utf-8') as f:
                f.write(text)
            # print(text)

    def parseChapterPage(self,chapterUrl):

        req=requests.get(self.base_Url+chapterUrl,headers=self.headers)
        req.encoding=self.encoding
        # print(req.text)
        html_tree=etree.HTML(req.text)
        div=html_tree.xpath('/html/body/div[2]/table')[0]
        h=html2text.HTML2Text()
        h.ignore_links=True
        text=h.handle(etree.tostring(div, pretty_print=True).decode())
        return text


pc=ParseChapter()
pc.start()