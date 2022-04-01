#! /usr/bin/env python  
# -*- coding:utf-8 -*-

from goose import Goose
from goose.text import StopWordsChinese
# 初始化，设置中文分词
g = Goose({'stopwords_class': StopWordsChinese})
# 文章地址
url = 'https://www.cnblogs.com/zhanghaohong/'
# 获取文章内容
article = g.extract(url=url)
# 标题
print ('标题：', article.title)
# 显示正文
print (article.cleaned_text)
print (article.top_image.src)
fp = open('E:\\test\\article.txt', 'ab')
fp.write(article.cleaned_text)
fp.close()