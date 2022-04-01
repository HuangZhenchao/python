import sys
from lxml import etree
from addBookmark import addBookmark 

workDir=""
def parseNode(node,tag):
    #print(etree.tostring(node).decode('utf-8'))
    #print(len(node.xpath("./*")),len(node.xpath("./dt")))
    #print(etree.tostring(node.xpath("./dl/dt")[0]).decode('utf-8'))
    lastTag=""
    for each in node.xpath("./*"):
        
        if each.tag=="dt":
            if len(each.xpath("./h3"))>0:
                lastTag=each.xpath("./h3/text()")[0]
            
            if len(each.xpath("./a"))>0:
                url=each.xpath("./a/@href")[0]
                title=each.xpath("./a/text()")[0]
                # print(url,title,tag)
                addBookmark(workDir,url,title,tag)
        else:
            parseNode(each,lastTag if tag=="" else tag+";"+lastTag)
        
        


def parseHTML(filePath):
    #parser = etree.HTML(encoding="utf-8")
    #xmlTree = etree.parse(filePath, parser=parser)  # 查看解析出的tree的内容
    htmlString=""
    with open(filePath,'r',encoding="utf-8") as fr:
        htmlString=fr.read()
    htmlString=htmlString.replace("</A>","</A></DT>").replace("</H3>","</H3></DT>")
    htmlString=htmlString.replace("</DT></DT>","</DT>")
    #pos=htmlString.rfind("</DT>")
    #htmlString=htmlString[:pos]
    xmlTree=etree.HTML(htmlString)

    root=xmlTree.xpath('//body/dl')[0]
    parseNode(root,"")

if __name__ == "__main__":
    workDir=sys.argv[1]# if sys.argv[1] else r"E:\avideo"
    filePath=sys.argv[2]
    parseHTML(filePath)