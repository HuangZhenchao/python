#! /usr/bin/env python  
# -*- coding:utf-8 -*-
import requests

from readability.readability import Document
response=requests.get('https://blog.csdn.net/qq_42156420/article/details/80784673')
#doc=Document(response.content)

readable_article=Document(response.content).summary()
readable_title=Document(response.content).short_title()
print ('readable_article: ',readable_article)
print ('readable_title: ',readable_title)
