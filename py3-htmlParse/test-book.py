#! /usr/bin/env python  
# -*- coding:utf-8 -*-
import csv
import os
import time

import requests
import html2text
from lxml import etree

headers = {
    'user-agent':"Mozilla/5.0 (Windows NT 6.1; Win64; x64)" "AppleWebKit/537.36 (KHTML, like Gecko)" "Chrome/68.0.3440.106" "Safari/537.36"
}
domain_url='http://www.guoxuedashi.com'
base_dir='D:\\OneNoteTempFile\\'
def get_book_info():
    for i in range(4,12):
        list=['','史部','子部','集','诗','儒','易','艺','医','丛','道','佛']
        dir=base_dir+list[i]
        if not os.path.exists(dir):
            os.mkdir(dir)

        category_list_url=domain_url+'/'+str(i)+'/'
        print(category_list_url)
        req=requests.get(category_list_url,headers=headers, timeout=20)
        html_tree=etree.HTML(req.text)
        category_list=html_tree.xpath('//dl/dt/a')
        index_x=0
        # 获取类别列表，遍历
        for category in category_list:
            index_x+=1
            if i<5 and index_x<3:
                continue
            category_text=category.xpath('./text()')[0]
            print(category_text)
            category_dir=dir+'\\'+str(index_x)+category_text
            if not os.path.exists(category_dir):
                os.mkdir(category_dir)

            category_href=category.xpath('./@href')[0]
            book_list_url=domain_url+category_href
            req=requests.get(book_list_url,headers=headers, timeout=20)
            html_tree=etree.HTML(req.text)
            book_list=html_tree.xpath('//dl/dd/a')
            index_y=0
            for book in book_list:
                index_y+=1
                if i<5 and index_x<4 and index_y<28:
                    continue
                book_text=book.xpath('./text()')[0]
                print(category_text)
                book_dir=category_dir+'\\'+str(index_y)+book_text
                print(book_dir)
                if not os.path.exists(book_dir):
                    os.mkdir(book_dir)
                book_href=book.xpath('./@href')[0]
                chapter_list_url=domain_url+book_href

                parseBook(book_dir,chapter_list_url)

            # 获取书籍url
            #获取章节url
            #解析章节内容
            #四部/类别/书目/章节/

def parseBook(book_dir,chapter_list_url):
    i = 0
    status=False
    while i<10:
        i = i + 1
        try:
            req=requests.get(chapter_list_url,headers=headers, timeout=20)
            if req.status_code==200:
                status=True
                html_tree=etree.HTML(req.text)
                chapter_list=html_tree.xpath('//dl/dd/a')
                index_z=0
                for chapter in chapter_list:
                    index_z+=1
                    #if index_z<146:
                    #    continue
                    chapter_text=chapter.xpath('./text()')[0]
                    print(chapter_text)
                    chapter_href=chapter.xpath('./@href')[0]
                    content_url=domain_url+chapter_href
                    file_name=str(index_z)+chapter_text+'.txt'
                    file_path=book_dir+'\\'+file_name
                    getContent(content_url,file_path)
                break
        except:
            continue
    if not status:
        stu=[book_dir,chapter_list_url]
        write2csv('D:\\OneNoteTempFile\\info.csv', stu)

def getContent(content_url,file_path):
    i = 0
    status=False
    while i<10:
        i = i + 1
        try:
            # 重新请求网址，加入新的请求头的
            req=requests.get(content_url,headers=headers, timeout=20)
            if req.status_code == 200:
                status=True
                html_tree=etree.HTML(req.text)
                contentHtml=html_tree.xpath('//div[@id="infozj_txt"]')[0]
                h=html2text.HTML2Text()
                h.ignore_links=True
                # h.emphasis_mark='\n__'
                content=h.handle(etree.tostring(contentHtml, pretty_print=True).decode())

                with open(file_path,'w',encoding='utf-8') as f:
                    f.write(content)
                break
        except:
            continue
    if not status:
        stu=[file_path,content_url]
        write2csv('D:\\OneNoteTempFile\\info.csv', stu)
    time.sleep(1)

def write2csv(filedir, stu):
    # write file
    # 打开文件，追加a
    out = open(filedir, 'a')
    # 设定写入模式
    csv_write = csv.writer(out, dialect='excel')
    csv_write.writerow(stu)
    out.close()

get_book_info()

# getContent(content_url,file_path)
#parseBook('D:\\OneNoteTempFile\\史部\\1正史\\17《旧唐书》 ·(后晋)刘昫','http://www.guoxuedashi.com/a/17kcea/')
#start()

'''contentHtml=etree.HTML('<div>1<em>测试</em>2</div>')
h=html2text.HTML2Text()
h.ignore_links=True
h.emphasis_mark='\"'
content=h.handle(etree.tostring(contentHtml, pretty_print=True).decode())
print(content)'''
