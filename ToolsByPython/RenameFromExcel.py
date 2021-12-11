#!/usr/bin/python
# coding=utf-8
#从excel中读取对应文件名将文件重命名
#
import xlrd
import os
#import xlwt
#
workbook = xlrd.open_workbook(r'D:\Spider Resource\jilebox.com\video\jilevideo\avtt-701000.xlsx')
sheet2 = workbook.sheet_by_index(0) # sheet索引从0开始
cols1 = sheet2.col_values(0)
cols2=sheet2.col_values(1)
#print cols2[0]

path1=r"D:\视频\成人视频\国产\短视频md5".decode('utf-8')
path2=r"D:\视频\成人视频\国产\长视频".decode('utf-8')
path3=r"D:\视频\成人视频\国产\长视频稍次".decode('utf-8')
path=path3
files=os.listdir(path)

for each in files:
    #print each
    index=-1
    for col2 in cols2:
        index+=1
        if each==col2:

            old_file = os.path.join(path, each)
            new_file=os.path.join(path, str(int(cols1[index])) + '.mp4')
            print(old_file)
            print(new_file)
            os.rename(old_file, new_file)
            break

