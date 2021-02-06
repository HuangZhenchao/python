#!/usr/bin/python
# coding=utf-8
import os
import hashlib
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
#path=r"D:\视频\成人视频\国产\视讯直播".decode('utf-8')

path=(r"D:\视频1：待入库\待删").decode('utf-8')
files=os.listdir(path)
for file in files:
    old_file=os.path.join(path, file)
    new_file=os.path.join(path, FileMD5(old_file)+'##@jilebox%video&$##.mp4')
    print old_file
    print new_file
    os.rename(old_file, new_file)