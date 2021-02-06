# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv

class AppointsInfoPipeline(object):
    def __init__(self):
        # 打开文件，指定方式为写，利用第3个参数把csv写数据时产生的空行消除
        self.f = open("D:\\医院专家坐诊信息.csv","a",newline="")
        # 设置文件第一行的字段名，注意要跟spider传过来的字典key名称相同
        self.fieldnames = ["expertId","expertName","hospital","highlightText","department","expertLevel","satisfaction",
                           "appointHospitalName","dateNew","week","time","btnText"]
        # 指定文件的写入方式为csv字典写入，参数1为指定具体文件，参数2为指定字段名
        self.writer = csv.DictWriter(self.f, fieldnames=self.fieldnames)
        # 写入第一行字段名，因为只要写入一次，所以文件放在__init__里面
        self.writer.writeheader()
    def process_item(self, item, spider):
        self.writer.writerow(item)

        return item

    def close_spider(self,spider):
        #关闭爬虫时顺便将文件保存退出
        self.f.close()