import os
import sys
import configparser
config = configparser.RawConfigParser()
tagGroup={}
keys=[]
def outputBookmarks(workDir,lastfolderName):    
    for each in os.listdir(workDir):
        eachPath=os.path.join(workDir,each)
        if os.path.isdir(eachPath):
            folderName=each if lastfolderName=="" else lastfolderName+";"+each
            outputBookmarks(eachPath,folderName)
        if not each.endswith(".url"):
            continue
        
        config.read(eachPath,encoding="utf-8-sig")
        title=each.replace(".url","")
        url=config.get("InternetShortcut","URL")
        description=config.get("description","description")+";"+lastfolderName
        if description=="":
            description="默认"
        for tag in description.split(";"):

            if tag.strip()=="":
                continue
            if tag not in tagGroup.keys():
                keys.append(tag)
                tagGroup[tag]=[]
            tagGroup[tag].append((title,url))
    


if __name__ == "__main__":
    workDir=sys.argv[1]# if sys.argv[1] else r"E:\avideo"
    filePath=sys.argv[2]
    #workDir="D://bookmarks/颜值"# if sys.argv[1] else r"E:\avideo"
    #filePath="D://bookmarks/颜值/bookmarks.html"
    outputBookmarks(workDir,"")

    htmlString=""
    for key in keys:
        dtString="    <DT><H3>"+key+"</H3></DT>\n"
        dlString=""
        for bookmark in tagGroup[key]:
            dlString=dlString+"        <DT><A HREF=\""+bookmark[1]+"\">"+bookmark[0]+"</A></DT>\n"
        dlString="    <DL>\n"+dlString+"\n    </DL>\n"
        htmlString=htmlString+dtString+dlString
    htmlString="<DL>\n"+htmlString+"\n</DL>"
    with open(filePath,'w',encoding="utf-8") as fw:
        fw.write(htmlString)