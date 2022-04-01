# os自定义包，对os做一些符合自己编程习惯的调整
from ast import Str
import os
import csv
import re
from .zhtools.langconv import Converter

#print('os自定义包，对os做一些符合自己编程习惯的调整')
def osListFilePath(path):
    FilePathList=[]
    for file in os.listdir(path):
        FilePathList.append(os.path.join(path,file))
    return FilePathList


# 获取一个没有重复的文件名
def getNoDupName(dir,name):
    path=os.path.join(dir, name)
    if os.path.exists(path):
        index=name.rfind('.')
        newname=name[:index]+'-1'+name[index:]

        return getNoDupName(dir,newname)
    else:
        return name

# 对一个字符串进行Windows文件名格式处理
def fileNameFormat(name)->Str:
    name=re.sub(r'[/*:<>?"|\\]',"#",name)    
    if len(name)>100:
        name=name[:100]
    return name


# 繁体简体转换
def convertHant():
    with open('D:\\CalendarDate\\out.csv','r',encoding='utf-8') as A:
        with open('D:\\CalendarDate\\out1.csv','a',encoding='utf-8') as B:
            line = A.readline()
            while line:
                print(line)
                line=Converter('zh-hans').convert(line)
                B.write(line)
                line = A.readline()

# 写入csv文件
def write2csv(filedir, rowData):
    # write file
    # 打开文件，追加a
    with open(filedir, 'a',newline='',encoding='utf-8') as out:
        # 设定写入模式
        csv_write = csv.writer(out, dialect='excel')
        csv_write.writerow(rowData)


if __name__ == '__main__':
    convertHant()