#! /usr/bin/env python  
# -*- coding:utf-8 -*-

import shutil,os
import hashlib
import sqlite3
def AddMD5Value(path,value):
    conn = sqlite3.connect(path)
    print("Opened database successfully")
    c = conn.cursor()
    c.execute('INSERT INTO video_md5 (md5)VALUES (\''+value+'\');')
    print("插入一行")
    conn.commit()
    conn.close()

def IsExistInExcel(path,value):
    conn = sqlite3.connect(path)
    print("Opened database successfully")
    c = conn.cursor()
    c.execute('SELECT id FROM video_md5 WHERE md5=\'' + value + '\';')
    ret =c.fetchall()
    conn.commit()
    conn.close()
    if len(ret)==0:
        return False
    else:
        print("MD5已经存在")
        return True


def FileMD5(file_path,Bytes=1024):
    md5 = hashlib.md5()                        #创建一个md5算法对象
    with open(file_path,'rb') as f:              #打开一个文件，必须是'rb'模式打开
        while 1:
            data =f.read(Bytes)                  #由于是一个文件，每次只读取固定字节
            if data:                      #当读取内容不为空时对读取内容进行update
                md5.update(data)
            else:                        #当整个文件读完之后停止update
                break
    ret = md5.hexdigest()              #获取这个文件的MD5值
    return ret

dir="D:\视频2：待归档"
md5_path="D:\DownInfo.db"

#file_dir="D:\图片1：待入库\\".decode('utf-8')+str(i)
folders=os.listdir(dir)
index=0
for folder in folders:
    index+=1
    print(index)
    folder_dir=os.path.join(dir, folder)
    files=os.listdir(folder_dir)
    for file in files:
        file_path=os.path.join(folder_dir, file)

        value=FileMD5(file_path)
        if IsExistInExcel(md5_path, value):
            print(file_path)
            #os.remove(file_path)
            print(os.path.join(folder_dir, '重复' + file))
            os.rename(file_path, os.path.join(folder_dir, '重复' + file))
        else:
            AddMD5Value(md5_path, value)
