
from ntpath import join
import os
import configparser
import sys
config = configparser.RawConfigParser()
from pylib.description import Description

constContent='''[InternetShortcut]
URL=@URL
    
[description]
description=@description
'''
    
def fromDescription(workDir):
    desc=Description(workDir,";")
    for each in desc.listfile():
        eachName=each.fileName
        eachPath=os.path.join(workDir,eachName)
        eachDescription=";".join(each.fileDesc)
                
        if not os.path.exists(eachPath):
            continue
        if not os.path.isfile(eachPath) or not eachName.endswith(".url"):
            continue
        config.read(eachPath,encoding="utf-8-sig")
        url=config.get("InternetShortcut","URL")
        content=constContent.replace("@URL",url).replace("@description",eachDescription)

        with open(eachPath,'w',encoding="utf-8") as fw:
            fw.write(content)

def trav(dir):
    fromDescription(dir)
    for each in os.listdir(dir):
        path=os.path.join(dir,each)
        if os.path.isdir(path):
            fromDescription(path)


if __name__ == "__main__":
    workDir=sys.argv[1]# if sys.argv[1] else r"E:\avideo"
    trav(workDir)
    