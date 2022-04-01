import os
from lxml import etree
import re
import html2text


def tra(dir):
    files = os.listdir(dir)
    for each in files:
        eachPath = os.path.join(dir, each)
        if os.path.isdir(eachPath):            
            tra(eachPath)
        else:            
            handleFile(eachPath)        


def handleFile(filepath):
    parser = etree.XMLParser(encoding="utf-8")
    xmlTree = etree.parse(filepath, parser=parser)  # 查看解析出的tree的内容
    # print(etree.tostring(xmlTree,encoding = 'utf-8').decode('utf-8'))
    for note in xmlTree.xpath('//note'):
        title = note.xpath('.//title/text()')[0]
        title=re.sub(r'[/*:<>?"|\\]',"#",title)
        if len(title)>100:
            title=title[:100]
        content = note.xpath('.//content/text()')[0]

        newFolderPath = filepath.replace(".enex", "")
        print(newFolderPath)
        if not os.path.exists(newFolderPath):
            os.mkdir(newFolderPath)
        newFilePath = os.path.join(newFolderPath, title+".html")

        handleNoteContent(newFilePath,content)



def handleNoteContent(filePath,content):
    h = html2text.HTML2Text()
    h.ignore_links = True
    text = h.handle(content).replace("\n\n", "\n")
    pList = text.split("\n")
    html = ""
    for p in pList:
        p = p.strip()
        if p == "":
            continue
        html = html+"<p>"+p+"</p>\n"
    # print(title,text)

    with open(filePath, "w", encoding="utf-8") as fw:
        content = fw.write(html)
        


workDir="D:\\0图书库\\四库文本enex格式"
tra(workDir)
