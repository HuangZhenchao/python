#! /usr/bin/env python  
# -*- coding:utf-8 -*-
import os
import sqlite3
import re

for i in range(820,830):
    file_dir="D:\视频2：待归档\\".decode('utf-8')+str(i)
    files=os.listdir(file_dir)
    index=0
    for each in files:
        index+=1
        print i,index
        id=re.findall(r'##@jilebox%video&(.*)\$##.mp4',each)[0]
        print id

        conn = sqlite3.connect('E:/videoID.db')
        c = conn.cursor()
        sqlstr='INSERT INTO tVideoID (videoID,state)VALUES ({},{});'.format(id,1)
        print sqlstr
        c.execute(sqlstr)
        conn.commit()
        conn.close()