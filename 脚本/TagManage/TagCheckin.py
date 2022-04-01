import hashlib
import os
import sys
import configparser
config = configparser.ConfigParser()

#对于没有备注的新增文件
from random import uniform


listIgnoreFile=['descript.ion','md5.txt','tmpmd5.txt','tmp.ion','dupfile.txt','md5.tmp']


# 对新增文件或文件名新加了tag的文件进行处理
# 思路：把已有的tag附在文件前面，统一进行分割提取
def checkin(dir):
    pathIon=os.path.join(dir,'descript.ion')
    pathTmpIon=os.path.join(dir,'tmp.ion')
    fileInDes= {}
    # 从descript.ion中读取文件和tag，以文件名作为key，拼接tag和name作为value
    if os.path.exists(pathIon):
        with open(pathIon, 'r', encoding='gbk',errors='ignore') as f_r:
            for line in f_r.readlines():
                line=line.replace("\n","")
                if line.startswith("\""):
                    pos=line.find("\" ",2)
                    if pos==-1:
                        continue
                    name=line[:pos+1].replace("\"","")
                    tag=line[pos+2:]
                    fileInDes[name]=tag.replace("*",";")+name

                else:
                    pos=line.find(" ")
                    if pos==-1:
                        continue
                    name=line[:pos]
                    tag=line[pos+1:].replace("*",";")
                    fileInDes[name]=tag+name

    for eachfile in os.listdir(dir):
        eachfilePath = os.path.join(dir, eachfile)
        if os.path.isdir(eachfilePath):
            checkin(eachfilePath)
        if eachfile in listIgnoreFile:
            continue
        if eachfile not in fileInDes:
            fileInDes[eachfile]=eachfile
            print('新增文件',eachfilePath)

    with open(pathTmpIon, 'w', encoding='gbk',errors='ignore') as f_w:
        for key in fileInDes:
            oldname=key
            oldpath=os.path.join(dir, oldname)
            if not os.path.exists(oldpath):
                continue
            namewithtag=fileInDes[key]

            pos=namewithtag.rfind(";")
            newname=namewithtag[pos+1:] if pos>-1 else namewithtag
            tag=namewithtag[:pos+1] if pos>-1 else ""
            #把不在gbk编码里的字符去掉
            newname=newname.encode('gbk','ignore').decode('gbk')
            #TODO:同名情况处理
            if not oldname==newname:
                newname=getNoDupName(dir,newname)
                print('last',newname)
                newpath=os.path.join(dir, newname)
                print('文件重命名',oldpath,newpath)

                os.rename(oldpath,newpath)

            if newname.find(" ")>-1:
                newname="\""+newname+"\""
            f_w.write(newname+" "+tag+"\n")



    if os.path.exists(pathIon):
        os.remove(pathIon)
    os.rename(pathTmpIon,pathIon)

def getNoDupName(dir,name):
    path=os.path.join(dir, name)
    if os.path.exists(path):
        index=name.rfind('.')
        newname=name[:index]+'-1'+name[index:]
        print(newname)
        return getNoDupName(dir,newname)
    else:
        return name

'''
config.read('./TagCheckin.ini')
section="dir"
for key in config.options(section):
    value = config.get(section,key)

    print(value)
    checkin(value)
'''
if __name__ == "__main__":
    workDir=sys.argv[1] if sys.argv[1] else r"E:\avideo"
    checkin(workDir)

#workdir=os.getcwd()
#checkin(workdir)
