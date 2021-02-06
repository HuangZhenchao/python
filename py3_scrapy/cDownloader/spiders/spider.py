# -*- coding: utf-8 -*-
import scrapy
import os
import time
import csv
import json
from ..items import AppointsInfoItem
class JileSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['https://expert.baidu.com/']

    start_urls = ['https://expert.baidu.com/med/page/gh/hospitaldetail?'
                  'title=广州市番禺区中医院&resource_id=5423&hospital=广州市番禺区中医院'
                  '&atn=hospitaldetail&sf_ref=search_gh_4334_depttitle&lid=9218550309&referlid=9218550309']

    def parse(self, response):
        urlstr='https://expert.baidu.com/med/api/gh/getexpertList?' \
            'vn=med&sf_ref=search_gh_4334_depttitle,search_gh_4334_depttitle&act=getexpertList&' \
            'hospital=广州市番禺区中医院&department={}&resource_id=5423&title={}' \
            '&atn=expertlist&lid=9218550309&referlid=9218550309&page=1&pageSize=10&applid='
        jsondata=json.loads(response.text)
        departslist=jsondata['data']['departsList']
        count=0
        for departs in departslist:
            if departs['text']=='热门科室':
                continue
            for depart in departs['options']:
                url=urlstr.format(depart['value'],depart['value'])
                print(url)
                yield scrapy.Request(url=url,callback=self.getExpertList,meta={"department":depart['value']},dont_filter=True)

    def getExpertList(self,response):
        # 获取专家列表
        print(1)
        urlstr='https://expert.baidu.com/med/page/gh/appointslistv1?resource_id=5423&sf_ref=search_gh_4334_depttitle' \
            '&title=挂号信息&expertId={}&department={}'
        print(urlstr)
        jsondata=json.loads(response.text)
        expertList=jsondata['data']['expertList']
        count=0
        for expert in expertList:
            expertId=expert['expertId']
            department=response.meta['department']
            url=urlstr.format(expertId,department)
            # 用专家的id：expertid去获取出诊医院信息及挂号信息
            print(count)
            print(url)
            yield scrapy.Request(url=url,callback=self.getAppointslist,dont_filter=True)

    def getAppointslist(self,response):
        item=AppointsInfoItem()
        # yield item
        jsondata=json.loads(response.text)
        expert=jsondata['data']['expert']
        for hospital in jsondata['data']['hospital']:
            for appoint in hospital['appointsList']:
                for date in appoint['dategroup']:
                    item['appointHospitalName']=hospital['hospitalName']
                    item['dateNew']=date['dateNew']
                    item['week']=date['week']
                    item['time']=date['time']
                    item['btnText']=date['btnText']

                    item['expertId']=expert['expertId']
                    item['expertName']=expert['expertName']
                    item['hospital']=expert['hospital']
                    item['highlightText']=jsondata['data']['highlightText']
                    item['department']=expert['department']
                    item['expertLevel']=expert['expertLevel']
                    item['satisfaction']=expert['satisfaction']

                    print(dict(item))
                    yield item
                    # .encode('latin-1').decode('unicode_escape')

