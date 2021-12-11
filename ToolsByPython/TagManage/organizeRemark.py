import hashlib
import os

#对于没有备注的新增文件
class organize:
    def __init__(self,workdir,videoHubDir):
        self.workdir=workdir
        self.lFileInHub=[]
        self.lFileTarget=[]
        self.lFileDub=[]

        self.Traverse(workdir)
        self.GetFileInHub(videoHubDir)
        self.FindDupFile()
        print(self.lFileDub)
        with open(workdir+'\\dupfile.txt','w') as f:
            f.writelines(self.lFileDub)

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

    def Traverse(self,dir):
        with open(os.path.join(dir,'descript.ion'), 'w', encoding='gbk',errors='ignore') as f_w:
            for file in os.listdir(dir):
                if file in ['descript.ion','tmp.ion','dupfile.txt']:
                    continue
                filePath = os.path.join(dir, file)
                if os.path.isdir(filePath):
                    self.Traverse(filePath)
                    continue
                md5 = organize.FileMD5(filePath)
                ext=file[file.rfind('.'):]
                newName=md5+ext
                newFilePath=os.path.join(dir, newName)

                strDescription=self.GetDescription(file)
                self.lFileTarget.append((newName,newFilePath))
                f_w.write(newName+' '+strDescription+'\n')
                if not os.path.exists(newFilePath):
                    os.rename(filePath,newFilePath)

    def GetDescription(self,file):
        print(file)
        strDescription=''
        lsTagPair=[]
        title=file
        if file.find(';')>-1:
            lRemark=file[:file.rfind(';')].split(";")
            title=file[(file.rfind(';')+1):]
            for remark in lRemark:
                tagGroup,tag=self.HandlerTag(remark)
                if tagGroup=='':
                    continue
                lsTagPair.append('%s:%s*'%(tagGroup,tag))
        for tagGroup in ['grade','classify','person','face','mosaic','female','uniform','relation','mating','ejaculation','outstanding','tag']:
            flag=False
            for sTagPair in lsTagPair:
                if sTagPair.startswith(tagGroup):
                    flag=True
                    strDescription=strDescription+sTagPair
                    continue
            if not flag:
                strDescription=strDescription+'%s:%s*'%(tagGroup,'')
        strDescription=strDescription+'%s:%s*'%('title',title)
        # strDescription='grade:*classify:*person:*face:*mosaic:*female:*uniform:*relation:*mating:*ejaculation:*outstanding:*tag:*title:%s*'
        return strDescription

    def HandlerTag(self,tag):
        if tag in ['A','B','C','D','E','S','N']:
            return 'grade',tag
        if tag in ['AI','91','pornhub','短视频','二次元','国产AV','国产三级','国产探花','国产网红','国产直播','国产自拍','欧美AV',
                   '日本AV无码','日本AV系列-fc2','日本AV系列-1pon','日本AV系列-10mu','日本AV系列-1000girl','日本AV系列-carib','日本AV系列-paco','日本AV系列-heyzo','日本AV系列-MK','日本AV系列-SKY','日本AV系列-SM','日本AV系列-Tokyo Hot',
                   '日韩三级','日韩自拍','摄影写真']:
            return 'classify',tag
        if tag.find('@')>-1:
            return 'person',tag

        if tag in ['清秀','颜值','骚货','正妹','邻家','少妇','少女','萝莉']:
            return 'female',tag

        if tag in ['牛仔','情趣','口罩','校服','猫女','妖精','体操','礼服','睡衣','模特','泡姬','丝袜','教师','空姐','女仆','网袜','面具','鼻环','眼镜','护士','眼罩','黑丝','JK','OL','cos','制服','学生','汉服','女警','兔女郎']:
            return 'uniform',tag

        if tag in ['约啪','妻子','伦理','女友','偷情']:
            return 'relation',tag

        if tag in ['手交','迷奸','器具','乱交','骑乘','乳交','肛交','后入','调教','双飞','女女','足交','多P','口交','自慰']:
            return 'mating',tag

        if tag in ['颜射','口爆','狂射','内射']:
            return 'ejaculation',tag

        if tag in ['美胸','KTV','户外','表情','淫叫','露出','呻吟','媚','贫乳','丰满','嘴','巨乳','野外','车上','骨感','长发','内窥','孕妇','美臀','高挑','短发','身材','大屌','对白','无毛','处女','美穴','特别','美足','美乳','美腿','公共场所','电话','黑白']:
            return 'outstanding',tag
        return 'tag',tag

    def FindDupFile(self):
        for fileTarget in self.lFileTarget:
            if fileTarget[0] in self.lFileInHub:
                self.lFileDub.append(fileTarget[1])

    def GetFileInHub(self,videoHubDir):
        for file in os.listdir(videoHubDir):
            if file=='descript.ion':
                continue
            path=os.path.join(videoHubDir,file)
            if os.path.isdir(path):
                self.GetFileInHub(path)
            else:
                self.lFileInHub.append(file)

def tmp(dir):
    descriptPath=os.path.join(dir,'descript.ion')

    with open(descriptPath,'r',encoding='gbk') as f:
        for line in f.readlines():

            strFile=line.split(" ")[0]
            path=os.path.join(dir,strFile)
            strRemakes=line.split(" ")[1].replace('\n','')
            strNewFileName=strRemakes+strFile
            strNewFilePath=os.path.join(dir,strNewFileName)
            os.rename(path,strNewFilePath)

#organize("E:\\0入库",r'E:\node_man\video')
tmp("E:\\000")