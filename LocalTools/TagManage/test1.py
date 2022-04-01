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
            print(newName+' '+fileName+';'+fileTag+'\n')

            newFilePath=os.path.join(self.workDir, newName)
            if not os.path.exists(newFilePath):
                os.rename(filePath,newFilePath)

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


def WriteToCsv(workDir,csvPath_av,csvPath_tagAll,csvPath_tagNotNull):
    ionPath=os.path.join(workDir, 'descript.ion')
    if os.path.exists(ionPath):
        with open(ionPath, 'r', encoding='gbk',errors='ignore') as f_read:
            csvW_t_av=csv.writer(open(csvPath_av, 'a', encoding='utf-8',newline=''),delimiter='#')
            csvW_t_tagAll=csv.writer(open(csvPath_tagAll, 'a', encoding='utf-8',newline=''),delimiter='#')
            csvW_t_tagNotNull=csv.writer(open(csvPath_tagNotNull, 'a', encoding='utf-8',newline=''),delimiter='#')
            for line in f_read.readlines():
                # print(workDir,line)
                listSplite = line.split(" ")
                fileName=listSplite[0]
                remarks=listSplite[1].replace('\n','')
                remarks=remarks.replace('；',';')
                oldName=remarks
                tagGroupList=[]
                folders=['E:\\AV\\AI','E:\\AV\\91','E:\\AV\\pornhub','E:\\AV\\短视频','E:\\AV\\二次元','E:\\AV\\国产AV','E:\\AV\\国产三级','E:\\AV\\国产探花','E:\\AV\\国产网红','E:\\AV\\国产直播','E:\\AV\\国产自拍','E:\\AV\\欧美AV','E:\\AV\\日本AV番号-不知道番号','E:\\AV\\日本AV番号-多个数量少的系列','E:\\AV\\日本AV番号-fc2','E:\\AV\\日本AV番号-日期番号-1pon',
                         'E:\\AV\\日本AV番号-日期番号-10mu','E:\\AV\\日本AV番号-日期番号-1000giri','E:\\AV\\日本AV番号-日期番号-carib','E:\\AV\\日本AV番号-日期番号-paco','E:\\AV\\日本AV番号-序号番号-heyzo','E:\\AV\\日本AV番号-序号番号-MK','E:\\AV\\日本AV番号-序号番号-sky','E:\\AV\\日本AV番号-序号番号-SM','E:\\AV\\日本AV番号-序号番号-TokyoHotn','E:\\AV\\日本AV-日本无码','E:\\AV\\日本AV-日本有码','E:\\AV\\日韩三级','E:\\AV\\日韩自拍','E:\\AV\\摄影写真']
                classifies=['AI','91','pornhub','短视频','二次元','国产AV','国产三级','国产探花','国产网红','国产直播','国产自拍','欧美AV','日本AV无码','日本AV无码','日本AV系列-fc2','日本AV系列-1pon','日本AV系列-10mu','日本AV系列-1000girl','日本AV系列-carib','日本AV系列-paco','日本AV系列-paco','日本AV系列-heyzo','日本AV系列-MK','日本AV系列-SM','日本AV系列-Tokyo Hot','日本AV无码','日本AV有码','日韩三级','日韩自拍','摄影写真']
                for i,folder in enumerate(folders):
                    if workDir.startswith(folder):
                        csvW_t_tagAll.writerow([fileName,'classify',classifies[i]])
                        tagGroupList=['classify']
                print(tagGroupList)
                if remarks.find(';')>-1:
                    for index,remark in enumerate(remarks.split(';')):
                        if remark =='' and index==len(enumerate(remarks.split(';')))-1:
                            continue
                        if index==0:
                            oldName=remark
                        else:
                            tag=remark
                            print(workDir+'\\'+fileName,tag)
                            print(tagGroupList)
                            tagGroupList.extend(HandlerTag(csvW_t_tagAll,fileName,tag))


                if oldName=='':
                    oldName=fileName
                csvW_t_av.writerow([fileName,workDir+'\\'+fileName,oldName])
                for tagGroup in ['classify','grade','face','mosaic','person','female','uniform','relation','mating','ejaculation','outstanding','tag']:
                    if tagGroup in tagGroupList:
                        continue
                    csvW_t_tagAll.writerow([fileName,tagGroup,''])
    for file in os.listdir(workDir):
        newPath=os.path.join(workDir,file)
        if os.path.isdir(newPath):
            WriteToCsv(newPath,csvPath_av,csvPath_tagAll,csvPath_tagNotNull)

def HandlerTag(csvW,fileName,tag):

    if tag in ['A','A0','A1','A2','A3','B','B0','B1','B2','B3','C0','C1','C2','C']:
        if tag=='A':
            csvW.writerow([fileName,'grade','N'])
            csvW.writerow([fileName,'face','露脸'])
            csvW.writerow([fileName,'mosaic','无码'])
        if tag=='A0':
            csvW.writerow([fileName,'grade','A'])
            csvW.writerow([fileName,'face','露脸'])
            csvW.writerow([fileName,'mosaic','无码'])
        if tag=='A1':
            csvW.writerow([fileName,'grade','B'])
            csvW.writerow([fileName,'face','露脸'])
            csvW.writerow([fileName,'mosaic','无码'])
        if tag=='A2':
            csvW.writerow([fileName,'grade','C'])
            csvW.writerow([fileName,'face','露脸'])
            csvW.writerow([fileName,'mosaic','无码'])
        if tag=='A3':
            csvW.writerow([fileName,'grade','D'])
            csvW.writerow([fileName,'face','露脸'])
            csvW.writerow([fileName,'mosaic','无码'])
        if tag=='B':
            csvW.writerow([fileName,'grade','N'])
            csvW.writerow([fileName,'face','不露脸'])
            csvW.writerow([fileName,'mosaic','无码'])
        if tag=='B0':
            csvW.writerow([fileName,'grade','A'])
            csvW.writerow([fileName,'face','不露脸'])
            csvW.writerow([fileName,'mosaic','无码'])
        if tag=='B1':
            csvW.writerow([fileName,'grade','B'])
            csvW.writerow([fileName,'face','不露脸'])
            csvW.writerow([fileName,'mosaic','无码'])
        if tag=='B2':
            csvW.writerow([fileName,'grade','C'])
            csvW.writerow([fileName,'face','不露脸'])
            csvW.writerow([fileName,'mosaic','无码'])
        if tag=='B3':
            csvW.writerow([fileName,'grade','D'])
            csvW.writerow([fileName,'face','不露脸'])
            csvW.writerow([fileName,'mosaic','无码'])
        if tag=='C':
            csvW.writerow([fileName,'grade','N'])
            csvW.writerow([fileName,'face','露脸'])
            csvW.writerow([fileName,'mosaic','有码'])
        if tag=='C0':
            csvW.writerow([fileName,'grade','A'])
            csvW.writerow([fileName,'face','露脸'])
            csvW.writerow([fileName,'mosaic','有码'])
        if tag=='C1':
            csvW.writerow([fileName,'grade','B'])
            csvW.writerow([fileName,'face','露脸'])
            csvW.writerow([fileName,'mosaic','有码'])
        if tag=='C2':
            csvW.writerow([fileName,'grade','C'])
            csvW.writerow([fileName,'face','露脸'])
            csvW.writerow([fileName,'mosaic','有码'])
        return ['grade','face','mosaic']
    delList=['虚拟','3D','三級','日本AV','日本码','主播','三级','国产AV','国产','韩国','国产自拍','二次元','亚裔','直播','日本','日本自拍','有码','欧美','不露脸','C10','D','D3',']']
    if tag in delList:
        return []

    sList=['[洗浴]','T]服务[','风俗','[制服][OL]','家教','老师','猫女仆','情侣','夫妻','女同','np','kj','两对','好穴','大长腿','窥阴','T]删[','待删','T]待删[']
    tList=['泡姬','泡姬','泡姬','OL','教师','教师','猫女','女友','妻子','女女','多P','口交','多P','美穴','美腿','内窥','可以删','可以删','可以删']
    for i,sTag in enumerate(sList):
        if tag==sTag:
            tag=tList[i]

    if tag in ['入江纱绫','大桥未久','中村ひかる','原小雪','中川美香','水谷心音','[碧木凛]',
               '小早川','百多えみり','姬川','优希','木村','沖瞳','北条麻妃','美月','神田','尾野真知子','羽月希','姬川优奈','麻仓优','雨宫琴音','爱沢']:
        tag='@'+tag

    if tag in ['蜜桃影视','糖心','糖心VLOG','果冻传媒','女优','精东影业','timi',
               'AI','网红','麻豆','swag','JVID','91']:
        tag=tag+'@'

    if tag.find('@')>-1:
        csvW.writerow([fileName,'person',tag])
        return ['person']

    if tag in ['清秀','颜值','骚货','正妹','邻家','少妇','少女','萝莉']:
        csvW.writerow([fileName,'female',tag])
        return ['female']

    if tag in ['牛仔','情趣','口罩','校服','猫女','妖精','体操','礼服','睡衣','模特','泡姬','丝袜','教师','空姐','女仆','网袜','面具','鼻环','眼镜','护士','眼罩','黑丝','JK','OL','cos','制服','学生','汉服','女警','兔女郎']:
        csvW.writerow([fileName,'uniform',tag])
        return ['uniform']

    if tag in ['约啪','妻子','伦理','女友','偷情']:
        csvW.writerow([fileName,'relation',tag])
        return ['relation']

    if tag in ['手交','迷奸','器具','乱交','骑乘','乳交','肛交','后入','调教','双飞','女女','足交','多P','口交','自慰']:
        csvW.writerow([fileName,'mating',tag])
        return ['mating']

    if tag in ['颜射','口爆','狂射','内射']:
        csvW.writerow([fileName,'ejaculation',tag])
        return ['ejaculation']

    if tag in ['美胸','KTV','户外','表情','淫叫','露出','呻吟','媚','贫乳','丰满','嘴','巨乳','野外','车上','骨感','长发','内窥','孕妇','美臀','高挑','短发','身材','大屌','对白','无毛','处女','美穴','特别','美足','美乳','美腿','公共场所','电话','黑白']:
        csvW.writerow([fileName,'outstanding',tag])
        return ['outstanding']
    csvW.writerow([fileName,'tag',tag])
    return ['tag']

if __name__ == "__main__":
    workDir = r"E:\AV"
    # CheckIn(workDir)
    WriteToCsv(workDir,workDir+'\\t_av.csv',workDir+'\\t_tagAll.csv',workDir+'\\t_tagNotNull.csv')