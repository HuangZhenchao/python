#! /usr/bin/env python  
# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import requests
import re

reBODY =re.compile( r'<body.*?>([\s\S]*?)<\/body>', re.I)
reCOMM = r'<!--.*?-->'
reTRIM = r'<{0}.*?>([\s\S]*?)<\/{0}>'
reTAG  = r'<[\s\S]*?>|[ \t\f\v]'

reIMG  = re.compile(r'<img[\s\S]*?src=[\'|"]([\s\S]*?)[\'|"][\s\S]*?>')

url='http://www.php.cn/python-tutorials-351066.html'
response = requests.get(url, timeout=5)
response.encoding = "UTF-8"

fp = open('E:\\test\\content.txt', 'wb')
fp.write(response.content)
fp.close()
withImage = reIMG.sub(r'{{\1}}', response.content)
withoutBODY = re.findall(reBODY, withImage)[0]
print withoutBODY
fp = open('E:\\test\\withoutBODY.txt', 'wb')
fp.write(withoutBODY)
fp.close()

withoutCOMM = re.sub(reCOMM, "", withoutBODY)
print withoutCOMM
fp = open('E:\\test\\withoutCOMM.txt', 'wb')
fp.write(withoutCOMM)
fp.close()

withoutStyle=re.sub(reTRIM.format("style"), "", withoutCOMM)
print withoutStyle
fp = open('E:\\test\\withoutStyle.txt', 'wb')
fp.write(withoutStyle)
fp.close()

withoutScript=re.sub(reTRIM.format("script"), "" ,withoutStyle)
print withoutScript
fp = open('E:\\test\\withoutScript.txt', 'wb')
fp.write(withoutScript)
fp.close()

withoutTag= re.sub(reTAG, "", withoutScript)
print withoutTag
fp = open('E:\\test\\withoutTag.txt', 'wb')
fp.write(withoutTag)
fp.close()