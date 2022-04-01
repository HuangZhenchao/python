#! /usr/bin/env python  
# -*- coding:utf-8 -*-
import os
import re
from selenium import webdriver

from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.binary_location="C:\myapp\\2Network tools\Browser\ChromePortable\App\Google Chrome\\chrome.exe"
chrome_options.add_argument('--headless')

chrome_options.add_argument('--disable-gpu')

driver = webdriver.Chrome(chrome_options=chrome_options)

driver.get("https://www.cnblogs.com/zhaof/p/6935473.html")

driver.set_window_size(1920,3600)

htmlNode=driver.find_elements_by_xpath('//body/child::*')
for node in htmlNode:
    width=node.value_of_css_property('width')
    height=node.value_of_css_property('height')
    print node.tag_name
    print width, height
    if width=='auto':
        elementWidth=0
    else:
        elementWidth=re.findall('(.*?)px', width)[0]
    if height == 'auto':
        elementHeight = 0
    else:
        elementHeight = re.findall('(.*?)px', height)[0]
    #print elementWidth,elementHeight
    if float(elementWidth)>500 and float(elementHeight)>500:
        print node.location
        #print node.value_of_css_property('top'),node.value_of_css_property('left')
        print node.value_of_css_property('width'),node.value_of_css_property('height')
        #print node.
#print htmlNode.text
#print driver.find_element_by_tag_name('body').value_of_css_property('width')
driver.save_screenshot("E:/selenium.png")
os.system('taskkill /im chrome.exe /t /F')
