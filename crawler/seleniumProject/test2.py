#! /usr/bin/env python  
# -*- coding:utf-8 -*-
'''
from bs4 import BeautifulSoup
import requests
response=requests.get('https://blog.csdn.net/mouday/article/details/81240257')

soup = BeautifulSoup(response.text,                      #HTML文档字符串
                         'html.parser',                  #HTML解析器
                         from_encoding = 'utf-8'         #HTML文档编码
                          )
for node in soup.body.children:
    print node.string
'''
import requests
import re
from pyquery import PyQuery as pq

def function(doc):
    pass


reCOMM = r'<!--.*?-->'
reTRIM = r'<{0}.*?>([\s\S]*?)<\/{0}>'
reLINK=r'<link .*?>|<link .*?\/>'
reTAG_A=r'<a .*?>'
reTAG  = r'<[\s\S]*?>|[ \t\f\v]'
reIMG = re.compile(r'<img[\s\S]*?src=[\'|"]([\s\S]*?)[\'|"][\s\S]*?>')
url='https://blog.csdn.net/iteye_7550/article/details/82330785'
response = requests.get(url, timeout=5)

withoutCOMM = re.sub(reCOMM, "", response.content)
withoutStyle=re.sub(reTRIM.format("style"), "", withoutCOMM)
withoutStyle=re.sub(reLINK, "", withoutStyle)
withoutScript=re.sub(reTRIM.format("script"), "" ,withoutStyle)
#withoutTag_A=re.sub(reTAG_A, "{{value:-20}}" ,withoutScript)
#withoutTag_A=reIMG.sub(r'{{img:\1}}', withoutTag_A)
#withoutTAG=re.sub(reTAG, "", withoutTag_A)
#print withoutTAG
#fp = open('E:\\test\\withoutScript.html', 'wb')
#fp.write(withoutScript)
#fp.close()
doc = pq(withoutScript)

#items=doc('#mainBox').children().items()
items=doc('body').children().items()
for node in items:
    if len(node.text())==0:
        node.remove()
        continue
    #print len(node.text()),node
    linkNodes=node.find('a').items()
    nodeWight=len(node.text())
    linkWight=2
    for linkNode in linkNodes:
        print nodeWight,linkWight
        linkWight=linkWight+2
        nodeWight=nodeWight-len(linkNode.text())-linkWight
        #if len(linkNode.parent().text())>len(linkNode.text()):
        #    count


