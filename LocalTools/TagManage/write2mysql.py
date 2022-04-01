import os

import pymysql
from pymysql.converters import escape_string


class write2mysql:
    def __init__(self, workDir):
        print("开始")
        self.workDir=workDir
        self.db=pymysql.connect(host='localhost',
                                user='node',
                                password='954325',
                                database='db_man',
                                autocommit=True)
        self.cursor = self.db.cursor()
        self.listFile=[]
        self.listTag=[]

        self.Traverse(workDir)

        self.createTable()
        self.insertFile()
        self.insertTag()
        print("结束")

    def __del__(self):
        self.db.close()

    def createTable(self):
        self.cursor.execute("DROP TABLE IF EXISTS t_video")
        sqlCreate_t_video="""CREATE TABLE t_video(
                            file varchar(255),
                            winpath varchar(255),
                            serpath varchar(255),
                            title  varchar(255),
                            INDEX `file`(`file`) USING BTREE)"""
        self.cursor.execute(sqlCreate_t_video)

        self.cursor.execute("DROP TABLE IF EXISTS t_videotag")
        sqlCreate_t_videotag="""CREATE TABLE t_videotag(
                            file varchar(255),
                            tagGroup varchar(255),
                            tag varchar(255) DEFAULT \'\',
                            INDEX `file`(`file`) USING BTREE,
                            INDEX `tagGroup`(`tagGroup`) USING BTREE,
                            INDEX `tag`(`tag`) USING BTREE)"""
        self.cursor.execute(sqlCreate_t_videotag)

    def insertFile(self):
        sql="insert into t_video values (%s,%s,%s,%s);"
        print('插入t_video',sql)
        try:
            # 执行SQL语句
            self.cursor.executemany(sql,self.listFile)
            # 提交修改
            self.db.commit()
            print('1')
        except:
            # 发生错误时回滚
            print('2')
            self.db.rollback()

    def insertTag(self):
        sql="insert into t_videotag values (%s,%s,%s);"
        print('插入t_videotag',sql)
        try:
            # 执行SQL语句
            self.cursor.executemany(sql,self.listTag)
            # 提交修改
            self.db.commit()
            print('1')
        except:
            # 发生错误时回滚
            self.db.rollback()
            print('2')

    def Traverse(self,workDir):
        ionPath=os.path.join(workDir, 'descript.ion')
        if os.path.exists(ionPath):
            with open(ionPath, 'r', encoding='gbk',errors='ignore') as f_read:
                for line in f_read.readlines():
                    # print(workDir,line)
                    listSplite = line.split(" ")
                    #分割备注，获取文件名
                    fileName=listSplite[0]
                    winPath=workDir+'\\'+fileName
                    projectPath="E:\\node_man"
                    serPath=winPath.replace(projectPath,'').replace('\\','/')
                    remarks=listSplite[1].replace('\n','').replace('；',';')
                    oldName=''
                    tagGroupList=[]
                    folders=['E:\\node_man\\video\\AI','E:\\node_man\\video\\91','E:\\node_man\\video\\pornhub','E:\\node_man\\video\\短视频','E:\\node_man\\video\\二次元','E:\\node_man\\video\\国产AV','E:\\node_man\\video\\国产三级','E:\\node_man\\video\\国产探花','E:\\node_man\\video\\国产网红','E:\\node_man\\video\\国产直播','E:\\node_man\\video\\国产自拍','E:\\node_man\\video\\欧美AV','E:\\node_man\\video\\日本AV番号-不知道番号','E:\\node_man\\video\\日本AV番号-多个数量少的系列','E:\\node_man\\video\\日本AV番号-fc2','E:\\node_man\\video\\日本AV番号-日期番号-1pon',
                             'E:\\node_man\\video\\日本AV番号-日期番号-10mu','E:\\node_man\\video\\日本AV番号-日期番号-1000giri','E:\\node_man\\video\\日本AV番号-日期番号-carib','E:\\node_man\\video\\日本AV番号-日期番号-paco','E:\\node_man\\video\\日本AV番号-序号番号-heyzo','E:\\node_man\\video\\日本AV番号-序号番号-MK','E:\\node_man\\video\\日本AV番号-序号番号-sky','E:\\node_man\\video\\日本AV番号-序号番号-SM','E:\\node_man\\video\\日本AV番号-序号番号-TokyoHotn','E:\\node_man\\video\\日本AV-日本无码','E:\\node_man\\video\\日本AV-日本有码','E:\\node_man\\video\\日韩三级','E:\\node_man\\video\\日韩自拍','E:\\node_man\\video\\摄影写真']
                    classifies=['AI','91','pornhub','短视频','二次元','国产AV','国产三级','国产探花','国产网红','国产直播','国产自拍','欧美AV','日本AV无码','日本AV无码','日本AV系列-fc2','日本AV系列-1pon','日本AV系列-10mu','日本AV系列-1000girl','日本AV系列-carib','日本AV系列-paco','日本AV系列-paco','日本AV系列-heyzo','日本AV系列-MK','日本AV系列-SM','日本AV系列-Tokyo Hot','日本AV无码','日本AV有码','日韩三级','日韩自拍','摄影写真']
                    for i,folder in enumerate(folders):
                        if workDir.startswith(folder):
                            self.listTag.append((fileName,'classify',classifies[i]))
                            tagGroupList=['classify']
                    # print(tagGroupList)
                    if remarks.find(';')>-1:
                        lRemark=remarks.split(';')
                        for index,remark in enumerate(lRemark):
                            if remark =='' and index==len(lRemark)-1:
                                #跳过最后一个；分割出的空字符串
                                continue
                            if index==0:
                                oldName=remark
                            else:
                                tag=remark
                                # print(workDir+'\\'+fileName,tag)
                                # print(tagGroupList)
                                tagGroupList.extend(self.HandlerTag(fileName,tag))

                    if oldName=='':
                        oldName=fileName

                    self.listFile.append((fileName,winPath,serPath,oldName))
                    for tagGroup in ['classify','grade','face','mosaic','person','female','uniform','relation','mating','ejaculation','outstanding','tag']:
                        if tagGroup in tagGroupList:
                            continue
                        self.listTag.append((fileName,tagGroup,''))
        for file in os.listdir(workDir):
            newPath=os.path.join(workDir,file)
            if os.path.isdir(newPath):
                self.Traverse(newPath)

    def HandlerTag(self,fileName,tag):

        if tag in ['A','A0','A1','A2','A3','B','B0','B1','B2','B3','C0','C1','C2','C']:
            if tag=='A':
                self.listTag.append((fileName,'grade','N'))
                self.listTag.append((fileName,'face','露脸'))
                self.listTag.append((fileName,'mosaic','无码'))
            if tag=='A0':
                self.listTag.append((fileName,'grade','S'))
                self.listTag.append((fileName,'face','露脸'))
                self.listTag.append((fileName,'mosaic','无码'))
            if tag=='A1':
                self.listTag.append((fileName,'grade','A'))
                self.listTag.append((fileName,'face','露脸'))
                self.listTag.append((fileName,'mosaic','无码'))
            if tag=='A2':
                self.listTag.append((fileName,'grade','B'))
                self.listTag.append((fileName,'face','露脸'))
                self.listTag.append((fileName,'mosaic','无码'))
            if tag=='A3':
                self.listTag.append((fileName,'grade','C'))
                self.listTag.append((fileName,'face','露脸'))
                self.listTag.append((fileName,'mosaic','无码'))
            if tag=='B':
                self.listTag.append((fileName,'grade','N'))
                self.listTag.append((fileName,'face','不露脸'))
                self.listTag.append((fileName,'mosaic','无码'))
            if tag=='B0':
                self.listTag.append((fileName,'grade','S'))
                self.listTag.append((fileName,'face','不露脸'))
                self.listTag.append((fileName,'mosaic','无码'))
            if tag=='B1':
                self.listTag.append((fileName,'grade','A'))
                self.listTag.append((fileName,'face','不露脸'))
                self.listTag.append((fileName,'mosaic','无码'))
            if tag=='B2':
                self.listTag.append((fileName,'grade','B'))
                self.listTag.append((fileName,'face','不露脸'))
                self.listTag.append((fileName,'mosaic','无码'))
            if tag=='B3':
                self.listTag.append((fileName,'grade','C'))
                self.listTag.append((fileName,'face','不露脸'))
                self.listTag.append((fileName,'mosaic','无码'))
            if tag=='C':
                self.listTag.append((fileName,'grade','N'))
                self.listTag.append((fileName,'face','露脸'))
                self.listTag.append((fileName,'mosaic','有码'))
            if tag=='C0':
                self.listTag.append((fileName,'grade','S'))
                self.listTag.append((fileName,'face','露脸'))
                self.listTag.append((fileName,'mosaic','有码'))
            if tag=='C1':
                self.listTag.append((fileName,'grade','A'))
                self.listTag.append((fileName,'face','露脸'))
                self.listTag.append((fileName,'mosaic','有码'))
            if tag=='C2':
                self.listTag.append((fileName,'grade','B'))
                self.listTag.append((fileName,'face','露脸'))
                self.listTag.append((fileName,'mosaic','有码'))
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
            self.listTag.append((fileName,'person',tag))
            return ['person']

        if tag in ['清秀','颜值','骚货','正妹','邻家','少妇','少女','萝莉']:
            self.listTag.append((fileName,'female',tag))
            return ['female']

        if tag in ['牛仔','情趣','口罩','校服','猫女','妖精','体操','礼服','睡衣','模特','泡姬','丝袜','教师','空姐','女仆','网袜','面具','鼻环','眼镜','护士','眼罩','黑丝','JK','OL','cos','制服','学生','汉服','女警','兔女郎']:
            self.listTag.append((fileName,'uniform',tag))
            return ['uniform']

        if tag in ['约啪','妻子','伦理','女友','偷情']:
            self.listTag.append((fileName,'relation',tag))
            return ['relation']

        if tag in ['手交','迷奸','器具','乱交','骑乘','乳交','肛交','后入','调教','双飞','女女','足交','多P','口交','自慰']:
            self.listTag.append((fileName,'mating',tag))
            return ['mating']

        if tag in ['颜射','口爆','狂射','内射']:
            self.listTag.append((fileName,'ejaculation',tag))
            return ['ejaculation']

        if tag in ['美胸','KTV','户外','表情','淫叫','露出','呻吟','媚','贫乳','丰满','嘴','巨乳','野外','车上','骨感','长发','内窥','孕妇','美臀','高挑','短发','身材','大屌','对白','无毛','处女','美穴','特别','美足','美乳','美腿','公共场所','电话','黑白']:
            self.listTag.append((fileName,'outstanding',tag))
            return ['outstanding']
        self.listTag.append((fileName,'tag',tag))
        return ['tag']


class FindDupFile:
    def __init__(self, workDir):
        self.file=[]
        self.dupFile=[]
        self.Traverse(workDir)
        print(self.dupFile)
        with open('E:\\node_man\\video\\dupfile.txt','w') as f:
            f.writelines(self.dupFile)

    def Traverse(self,workDir):
        for file in os.listdir(workDir):
            if file=='descript.ion':
                continue
            path=os.path.join(workDir,file)
            if os.path.isdir(path):
                self.Traverse(path)
            else:
                if file in self.file:
                    self.dupFile.append(path)
                else:
                    self.file.append(file)






#文件不存在（或路径改变）的先删除tgfmpcfurmeot

#数据库里不存在的则添加

#对新增文件进行处理

#FindDupFile
#write2mysql("E:\\node_man\\video")
#FindDupFile("E:\\node_man\\video")
