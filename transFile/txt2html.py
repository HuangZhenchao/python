#1、把TXT按章节分割
#2、每章分别存为html，把段落用p标签包裹
#
import os
import re
import sys
import chardet

#from types import NoneType
class TranscodeFile:
    types=["txt"]
    def __init__(self,path):
        if os.path.isdir(path):
            self.traversal(path)
        else:
            if path[path.rfind(".")+1:] in self.types:
                self.handleFile(path)

        
    def traversal(self,dir):
        files = os.listdir(dir)
        for each in files:
            eachPath = os.path.join(dir, each)
            if os.path.isdir(eachPath):            
                self.traversal(eachPath)
            else:
                if each[each.rfind(".")+1:] in self.types:
                    self.handleFile(eachPath)

    def isTitle(line):
        match1=re.match(r'^第（*[0123456789一二三四五六七八九十百千万]+）*[章节卷部]',line)
        match2=re.match(r'^（[0123456789一二三四五六七八九十百千万]+）',line)
        match3=re.match(r'[0123456789一二三四五六七八九十百千万]+[：、]*$',line)
        if match1 is None and match2 is None and match3 is None:
            return False
        return True

    def handleFile(self,filepath):
        chapters=[]
        lines=[]
        with open(filepath, "rb") as fr:
            filebytes=fr.read()
            print("duqu")
            encoding=chardet.detect(filebytes[0:1024])["encoding"]
            print(encoding)
            if encoding=="GB2312":
                encoding="GBK"
            lines=filebytes.decode(encoding,"ignore").split("\n")
                    
        lastTitle=os.path.basename(filepath).replace(".txt","")
        lastContent=""

        for line in lines:
            line=line.strip()
            if TranscodeFile.isTitle(line):
                self.handleChapter(filepath,lastTitle,lastContent)
                lastTitle=line
                lastContent=""                               
            else:
                lastContent=lastContent+"<p>"+line+"</p>\n"

        self.handleChapter(filepath,lastTitle,lastContent)

    def handleChapter(self,filepath,title,content):
        print(filepath,title)    
        folderpath=filepath.replace(".txt","")
        if not os.path.exists(folderpath):
            os.mkdir(folderpath)
            
        title=re.sub(r'[/*:<>?"|\\]',"#",title)
        if len(title)>100:
            title=title[:100]
        path=os.path.join(filepath.replace(".txt",""),title+".html")
        with open(path, "w", encoding="utf-8") as fw:
            fw.write(content)

        
print(sys.argv[1])
trans=TranscodeFile(sys.argv[1])