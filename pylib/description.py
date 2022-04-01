# descript.ion是对文件夹内文件得到描述备注
# 在total cmd中可以显示为列
# 此模块是对描述文件descript.ion的操作类
# 功能如下
# 1、解析文件为一个列表
from __future__ import annotations
from ast import Str
import os
from typing import List, Tuple

class DescItem:
    fileName:Str=""
    fileDesc:List[Str]=[]

    def __init__(self) -> None:
        self.fileName=""
        self.fileDesc=[]

    def __str__(self):
        print(self.fileName)
        for desc in self.fileDesc:
            print("     ",desc)


class Description:
    path:Str="1"
    list:List[DescItem]=[]
    separator=""
    def __init__(self,dir,separator) -> None:
        self.path=os.path.join(dir,"descript.ion")
        self.separator=separator
        if not os.path.exists(self.path):
            return None
        with open(self.path,'r') as fr:
            for line in fr.readlines():
                flag,item=self.handleLine(line)
                if flag:
                    self.list.append(item)

    def handleLine(self,line:Str)->Tuple(bool,DescItem):
        flag=True
        item=DescItem()

        line=line.replace("\n","")
        line=line.strip()
        if line=="":
            return False,None
        if line.startswith("\""):
            pos=line.find("\" ",2)
            if pos==-1:#如果以",又没有结束，则返回错误
                return False,None
            item.fileName=line[:pos+1].replace("\"","")
            description=line[pos+2:]
        else:
            pos=line.find(" ")
            if pos==-1:
                return False,None
            item.fileName=line[:pos]
            description=line[pos+1:]
        
        if self.separator!="":
            for eachDesc in description.split(self.separator):
                if eachDesc.strip()=="":
                    continue
                item.fileDesc.append(eachDesc)
        else:
            item.fileDesc.append(description)
            print(self.separator,item.__str__())
            
        return flag,item

    def listfile(self)->List[DescItem]:
        return self.list

    def clear():
        pass


if __name__ == "__main__":
    des=Description("D:\\",";")
    print(des.path,des.listfile())