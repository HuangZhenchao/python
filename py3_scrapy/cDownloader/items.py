# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AppointsInfoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    '''
    "expert": {
      "department": "门诊乳腺科",
      "expertId": "969216",
      "expertLevel": "主任医师",
      "expertName": "常旭",
      "hospital": "广州市番禺区中医院",
      "satisfaction": "86%",
      "highlightText": "乳腺外科",

    hospital->0->hospitalName
               ->appointsList->0->dategroup->list->0=>{
                    "btnText": "挂号",
                    "dateNew": "2020年11月23日",
                    "time": "上午",
                    "week": "周一"
                  }
    '''
    expertId=scrapy.Field()
    expertName=scrapy.Field() # 科室 专家名 日期 星期 上下午
    hospital=scrapy.Field()
    highlightText=scrapy.Field()
    department=scrapy.Field()
    expertLevel=scrapy.Field()
    satisfaction=scrapy.Field()
    appointHospitalName=scrapy.Field()
    dateNew=scrapy.Field()
    week=scrapy.Field()
    time=scrapy.Field()
    btnText=scrapy.Field()

