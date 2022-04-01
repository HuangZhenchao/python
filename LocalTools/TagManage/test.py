import csv
import hashlib
import os
'''
with open(descriptPath, 'r', encoding='gbk') as f:
    for line in f.readlines():
        strFileName = line.split(" ")[0]
        path = os.path.join(wordDir, strFileName)
        strRemakes = line.split(" ")[1]

        newpath = path + '#' + strRemakes + '.mp4'
        newpath = newpath.replace('\n', '')
        newpath = newpath.replace('\"', '')
        path = path.replace('\"', '')
        os.rename(path, newpath)
        print(path, newpath)
'''


class CheckIn:
    def __init__(self, workDir):
        self.workDir=workDir
        self.ionPath=os.path.join(workDir, 'descript.ion')
        self.tmpIonPath=workDir+'\\'+'tmp.ion'

        self.listNextDir=[]
        self.listFileWithTag = self.GetFileWithRemarks(workDir)

        self.fp_ion=open(self.tmpIonPath,'w',newline='',encoding='gbk')
        self.md5AsName()
        if os.path.exists(self.ionPath):
            os.remove(self.ionPath)
        self.fp_ion.close()
        os.rename(self.tmpIonPath,self.ionPath)
        for nextDir in self.listNextDir:
            CheckIn(nextDir)

    def md5AsName(self):
        # 计算md5，作为文件名，原文件名写入备注里
        for fileName in os.listdir(self.workDir):
            if fileName in ['descript.ion','tmp.ion']:
                continue
            filePath = os.path.join(self.workDir, fileName)
            if os.path.isdir(filePath):
                self.listNextDir.append(filePath)
                continue

            fileTag=self.GetRemarks(fileName)
            # 读取备注


            print(filePath,fileTag)
            # 生成MD5值，以md5重命名文件
            md5 = CheckIn.FileMD5(filePath)
            ext=fileName[fileName.rfind('.'):]
            newName=md5+ext
            newFilePath=os.path.join(self.workDir, newName)
            if not os.path.exists(newFilePath):
                os.rename(filePath,newFilePath)
            print(newName+' '+fileName+';'+fileTag+'\n')

            self.fp_ion.writelines(newName+' '+fileName+';'+fileTag+'\n')

    def GetRemarks(self,fileName):
        for eachFileWithTag in self.listFileWithTag:
            if fileName == eachFileWithTag['name']:
                return eachFileWithTag['tag']
        return ''

    def GetFileWithRemarks(self,workDir):
        # 读取descript.ion文件里的备注赋值
        listFileWithTag = []

        if os.path.exists(self.ionPath):
            with open(self.ionPath, 'r', encoding='gbk',errors='ignore') as f:
                for line in f.readlines():
                    # print(workDir,line)
                    fileName = line.split(" ")[0]
                    fileTag = line.split(" ")[1].replace('\n','')
                    fileInfo = \
                        {'name': fileName,
                         'path': os.path.join(workDir, fileName),
                         'tag': fileTag}
                    listFileWithTag.append(fileInfo)
        return listFileWithTag

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


def WriteToCsv(workDir,csvPath):
    ionPath=os.path.join(workDir, 'descript.ion')
    if os.path.exists(ionPath):
        with open(ionPath, 'r', encoding='gbk',errors='ignore') as f_read:
            with open(csvPath, 'a', encoding='utf-8',newline='') as f_write:#,errors='ignore'
                csv_w=csv.writer(f_write,delimiter='#')
                for line in f_read.readlines():
                    # print(workDir,line)
                    listSplite = line.split(" ")
                    fileName=listSplite[0]

                    listRearks = listSplite[1].replace('\n','').split(';',1)
                    print(listRearks)
                    csv_w.writerow([fileName,workDir+'\\'+fileName,listRearks[0],listRearks[1]])
    for file in os.listdir(workDir):
        newPath=os.path.join(workDir,file)
        if os.path.isdir(newPath):
            WriteToCsv(newPath,csvPath)


if __name__ == "__main__":
    workDir = r"E:\AV"
    cmd=2
    if cmd==1:
        for file in os.listdir(workDir):
            if file not in ['00','短视频']:#
                continue
            filePath=os.path.join(workDir, file)
            if os.path.isdir(filePath):
                print(filePath)
                CheckIn(filePath)
                # WriteToCsv(filePath,r"E:\AV\all.csv")
    if cmd==2:
        for file in os.listdir(workDir):
            if file in ['00','短视频']:#
                continue
            filePath=os.path.join(workDir, file)
            if os.path.isdir(filePath):
                print(filePath)
                # CheckIn(filePath)
                WriteToCsv(filePath,r"E:\AV\all.csv")