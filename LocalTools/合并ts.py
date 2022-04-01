#! /usr/bin/env python  

#import natsort
import time
import os
import re
import subprocess
#file_folder_dir="D:\视频1：待入库\\avtt37\shipin3\\toupaizipai\\0".encode('utf-8')
file_folder_dir="E:\\test\\0\\"
folders=os.listdir(file_folder_dir)
for folder in folders:
    if folder=='6':
        continue
    file_dir=os.path.join(file_folder_dir, folder)
    if os.path.isfile(file_dir):
        continue
    files=os.listdir(file_dir)
    print(files)
    #natsort.natsorted(files)
    files.sort(key=lambda x: int(re.sub('_','',x[:-3])))

    file_str=''
    for file in files:
        file_str=file_str+'file \'{}\'\n'.format(os.path.join(file_dir, file))
    print(file_str)
    path='G:\\temp'
    if not os.path.exists(path):
        os.makedirs(path)
    path='G:\\temp\\tsList.txt'
    with open(path,'w') as f:
        f.write(file_str)

    #file_str='85060_295_10.ts|85060_295_100.ts'
    tfile=os.path.join(file_folder_dir, folder + ".mp4")
    print(tfile)
    #os.chdir(file_dir)
    cmdstr='ffmpeg -y -f concat -safe 0 -i {} -c copy \"{}\"'.format(path,tfile)
    print(cmdstr)
    #os.system(cmdstr).decode('gbk')
    p=subprocess.Popen(cmdstr)
    p.communicate()
    #pipeline=os.popen(cmdstr)
    #text=pipeline.read()
    #print(text)
