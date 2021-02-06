#! /usr/bin/env python  
# -*- coding:utf-8 -*-
import sys
import requests
import html2text
reload(sys)
sys.setdefaultencoding('utf-8')
response=requests.get('https://blog.csdn.net/llf_cloud/article/details/84310644')
response.encoding='utf-8'
h=html2text.HTML2Text()
h.ignore_links=True
print h.handle(response.content)

