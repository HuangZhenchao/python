import os
import re
import sys
import pylib.osLib as osLib
import configparser

config = configparser.RawConfigParser()


def addBookmark(dir,url,title,description):
    # 编码转换
    title=title.encode('gbk','ignore').decode('gbk')
    description=description.encode('gbk','ignore').decode('gbk') 
    # 文件名格式处理
    title=osLib.fileNameFormat(title)+".url"
    path=os.path.join(dir,title)
    # 文件名则判断url是否相同
    if os.path.exists(path):
        config.read(os.path.join(dir,title),encoding="utf-8-sig")
        oldUrl=config.get("InternetShortcut","URL")
        #不同则取新名，相同则覆盖
        if oldUrl!=url:
            title=osLib.getNoDupName(dir,title)

    content='''[InternetShortcut]
URL=@URL
    
[description]
description=@description'''
    content=content.replace("@URL",url).replace("@description",description)
    path=os.path.join(dir,title)
    # print(path)
    # 写入.URL
    with open(path,'w',encoding="utf-8") as fw:
        fw.write(content)
    # 读取descript.ion，替换或新增
    descString=""
    try:
        with open(os.path.join(dir,"descript.ion"),"r") as fr:
            descString=fr.read()
    except:
        descString=""
    if title.find(" ")>-1:
        title="\""+title+"\""
    pattern="^"+re.escape(title)+"(.+?)$"
    pattern=re.compile(pattern,re.M)
    #print(pattern,re.search(re.escape("\n"+title+"(.+?)\n"),descString))
    replaceString=title+" "+description
    if re.search(pattern,descString):
        descString=re.sub(pattern,replaceString,descString)
    else:
        descString=descString+"\n"+replaceString  
        

    with open(os.path.join(dir,"descript.ion"),"w") as fw:        
        fw.write(descString)


if __name__ == "__main__":
    workDir=sys.argv[1]# if sys.argv[1] else r"E:\avideo"
    url=sys.argv[2]
    title=sys.argv[3]
    description=sys.argv[4]
    
    addBookmark(workDir,url,title,description)
