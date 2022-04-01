
import os
import sys
import configparser
from typing import Dict
config = configparser.RawConfigParser()

def getExists(dir,url)->None or Dict:
    for each in os.listdir(dir):
        path=os.path.join(dir,each)
        if os.path.isdir(path):
            result=getExists(path,url)
            if result is None:
                continue
            else:
                return result
        if not each.endswith(".url"):
            continue
        config.read(path,encoding="utf-8-sig")
        eachUrl=config.get("InternetShortcut","URL")
        if eachUrl==url:
            eachDescription=config.get("description","description")
            obj={
                "isExists":"True",
                "url":eachUrl,
                "title":each.replace(".url",""),
                "description":eachDescription,
            }
            return obj
    return None
    


if __name__ == "__main__":
    workDir=sys.argv[1]# if sys.argv[1] else r"E:\avideo"
    url=sys.argv[2]
    result=getExists(workDir,url)
    if result is None:
        print({
            "isExists":"False"
        })
    else:
        print(result)