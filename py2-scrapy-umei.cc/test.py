#!/usr/bin/python
# coding=utf-8
import requests
import time


response = requests.get('https://www.baidu.com/', verify=False, timeout=20)
print response.status_code