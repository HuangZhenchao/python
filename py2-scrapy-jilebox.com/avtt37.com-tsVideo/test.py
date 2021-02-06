#!/usr/bin/python
# coding=utf-8
import threading
import time
import requests
import os
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
class test():
    def __init__(self):
        pass

    def h(self):
        with ThreadPoolExecutor(2) as executor:
            for j in range(5):  # 新建5个线程 等待队列
                executor.submit(self.tTest, j)
                print('线程{}开始'.format(j))
        return 1

    def tTest(self,i):
        time.sleep(3)
        print('线程{}执行'.format(i))

print('开始')
i=0
i=test.h()
print(i)
print('结束')
time.sleep(50)