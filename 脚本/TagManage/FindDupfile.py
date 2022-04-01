import hashlib
import os
import configparser
config = configparser.ConfigParser()

def FileMD5(file_path,Bytes=1024):
    md5 = hashlib.md5()                        #创建一个md5算法对象
    with open(file_path,'rb') as f:              #打开一个文件，必须是'rb'模式打开
        while 1:
            data =f.read(Bytes)                  #由于是一个文件，每次只读取固定字节
            if data:                      #当读取内容不为空时对读取内容进行update
                md5.update(data)
            else:                        #当整个文件读完之后停止update
                break
    ret = md5.hexdigest()              #获取这个文件的MD5值
    return ret


listIgnoreFile=['descript.ion','tmp.ion']


class FindDupFile:
    def __init__(self,section,workdir):
        pathOut=os.path.join(os.getcwd(),"output")
        self.workdir=workdir
        self.lPath=[];self.dictMD5={};self.lDupFile=[];
        self.pathMD5=os.path.join(pathOut,section+".md5record")
        self.pathMD5Tmp=os.path.join(pathOut,section+".md5tmp")
        self.pathDup=os.path.join(pathOut,section+".md5dup")
        self.fw_md5RecordTmp=open(self.pathMD5Tmp, 'w', encoding='gbk',errors='ignore')
        self.fw_dupfile=open(self.pathDup, 'w', encoding='gbk',errors='ignore')

        self.listFileMd5(self.workdir)
        self.TraDir(self.workdir)

        self.fw_md5RecordTmp.close()
        self.fw_dupfile.close()
        if os.path.exists(self.pathMD5):
            os.remove(self.pathMD5)
        os.rename(self.pathMD5Tmp,self.pathMD5)

    def __del__(self):
        pass

    def handlerPath(self,path):
        path=("\""+path+"\"") if path.find(" ")>-1 else path
        return path

    def checkFileMD5(self,path,md5):
        if not os.path.exists(path):
            return
        self.lPath.append(path)

        if md5 in self.dictMD5:
            self.lDupFile.append((md5,self.dictMD5[md5]))
            self.lDupFile.append((md5,path))
            self.fw_dupfile.write(md5+" "+self.handlerPath(path)+"\n")
            self.fw_dupfile.write(md5+" "+self.handlerPath(self.dictMD5[md5])+"\n")
            print('重复',path)
        else:
            self.dictMD5[md5]=path
            self.fw_md5RecordTmp.write(self.handlerPath(path)+" "+md5+"\n")

    def listFileMd5(self,dir):
        if not os.path.exists(self.pathMD5):
            return
        with open(self.pathMD5, 'r', encoding='gbk',errors='ignore') as fr:
            for line in fr.readlines():
                line=line.replace("\n","")
                if line.startswith("\""):
                    pos=line.find("\" ",2)
                    if pos==-1:
                        continue
                    name=line[:pos+1].replace("\"","")
                    md5=line[pos+2:]
                    self.checkFileMD5(name,md5)
                else:
                    pos=line.find(" ")
                    if pos==-1:
                        continue
                    name=line[:pos]
                    md5=line[pos+1:]
                    self.checkFileMD5(name,md5)

    def TraDir(self,dir):
        for file in os.listdir(dir):
            path=os.path.join(dir,file)
            if os.path.isdir(path):
                self.TraDir(path)
                continue
            if file in listIgnoreFile:
                continue
            path=path.encode('gbk','ignore').decode('gbk')
            if path in self.lPath:
                continue
            print(path)
            self.checkFileMD5(path,FileMD5(path))




config.read('./FindDupfile.ini')

for section in config.sections():
    value = config.get(section,'workdir')
    fdp=FindDupFile(section,value)
    print(value)
