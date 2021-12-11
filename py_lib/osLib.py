print('os自定义包，对os做一些符合自己编程习惯的调整')
import os
import csv
from langconv import Converter
def osListFilePath(path):
    FilePathList=[]
    for file in os.listdir(path):
        FilePathList.append(os.path.join(path,file))
    return FilePathList

def convertHant():
    with open('D:\\CalendarDate\\out.csv','r',encoding='utf-8') as A:
        with open('D:\\CalendarDate\\out1.csv','a',encoding='utf-8') as B:
            line = A.readline()
            while line:
                print(line)
                line=Converter('zh-hans').convert(line)
                B.write(line)
                line = A.readline()
def write2csv(filedir, rowData):
    # write file
    # 打开文件，追加a
    with open(filedir, 'a',newline='',encoding='utf-8') as out:
        # 设定写入模式
        csv_write = csv.writer(out, dialect='excel')
        csv_write.writerow(rowData)
if __name__ == '__main__':
    convertHant()