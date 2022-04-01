import os
import sys
import pymysql


class TagManager:
    def __init__(self,workDir):
        self.workDir=workDir
        self.listFile=[]
        self.listTag=[]
        self.db=pymysql.connect(host='localhost',
                                user='node',
                                password='954325',
                                database='db_man')
        self.cursor = self.db.cursor()

    def __del__(self):
        self.db.close()

    def Export(self):
        sqlSetectDirs='select winpath from t_video GROUP BY winpath;'
        sqlSelectFile='''select a.*,b.tags from t_video a left join (select file,GROUP_CONCAT(tag SEPARATOR ';') as tags from t_videotag GROUP BY file) b on a.file=b.file where a.winpath=%s order by a.file'''

        self.cursor.execute(sqlSetectDirs)
        dirs = self.cursor.fetchall()
        for row in dirs:
            dir=row[0]
            self.cursor.execute(sqlSelectFile,dir)
            results=self.cursor.fetchall()
            #print(results)
            self.ParseResults(dir,results)


    def ParseResults(self,dir,results):
        tmpIonPath=os.path.join(dir,'tmp.ion')
        ionPath=os.path.join(dir,'descript.ion')
        with open(tmpIonPath, 'w', encoding='gbk',errors='ignore') as f_w:
            for result in results:
                file=result[1]
                #title=result[3]
                tag='' if result[4] is None else result[4]+";"
                #print(type(result[4]))
                if file.find(" ")>-1:
                    file="\""+file+"\""
                f_w.write(file+' '+tag+'\n')
        if os.path.exists(ionPath):
            os.remove(ionPath)
        os.rename(tmpIonPath,ionPath)

    def createTable(self):
        self.cursor.execute("DROP TABLE IF EXISTS t_video")
        sqlCreate_t_video="""CREATE TABLE t_video(
                            file varchar(255),
                            filename varchar(255),
                            winpath varchar(255),
                            serpath varchar(255),
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

    def Import(self):
        self.Traverse(self.workDir)
        self.createTable()
        self.insertFile()
        self.insertTag()

    def SplitLine(self,dir,line,delimit):
        pos=line.find(delimit,1)
        if pos==-1:
            return
        name=line[:pos].replace("\"","")
        #TODO:进行文件筛选，应该只把视频文件录进去
        winPath=dir+'\\'+name
        projectPath="E:"
        serPath=winPath.replace(projectPath,'').replace('\\','/')
        self.listFile.append((winPath,name,dir,serPath))
        tag=line[pos+len(delimit):]

        for eachtag in tag.split(";"):
            if eachtag=="":
                continue
            tagGroup=self.HandlerTag(eachtag)

            self.listTag.append((winPath,tagGroup,eachtag))


    def Traverse(self,dir):
        for file in os.listdir(dir):
            path=os.path.join(dir,file)
            if os.path.isdir(path):
                self.Traverse(path)
        ionPath=os.path.join(dir, 'descript.ion')
        if os.path.exists(ionPath):
            with open(ionPath, 'r', encoding='gbk',errors='ignore') as f_read:
                for line in f_read.readlines():
                    # print(workDir,line)
                    line=line.replace("\n","")
                    if line.startswith("\""):
                        self.SplitLine(dir,line,"\" ")
                    else:
                        self.SplitLine(dir,line," ")

    def HandlerTag(self,tag):

        if tag.find('@')>-1:
            return 'person'
        if tag in ['A','B','C','D','E','N']:
            return 'grade'

        if tag in ['露脸','半露脸','不露脸']:
            return 'face'

        if tag in ['有码','无码']:
            return 'mosaic'
        if tag in ['AI','91','pornhub','短视频','二次元','国产AV','国产三级',
                   '国产探花','国产网红','国产直播','国产自拍','欧美AV','日本AV无码','日本AV无码',
                   '日本AV系列-fc2','日本AV系列-1pon','日本AV系列-10mu','日本AV系列-1000girl',
                   '日本AV系列-carib','日本AV系列-paco','日本AV系列-paco','日本AV系列-heyzo',
                   '日本AV系列-MK','日本AV系列-SM','日本AV系列-Tokyo Hot','日本AV无码','日本AV有码',
                   '日韩三级','日韩自拍','摄影写真']:
            return 'classify'

        if tag in ['清秀','颜值','骚货','正妹','邻家','少妇','少女','萝莉']:
            return 'female'

        if tag in ['牛仔','情趣','口罩','校服','猫女','妖精','体操','礼服','睡衣','模特','泡姬','丝袜','教师','空姐','女仆','网袜','面具','鼻环','眼镜','护士','眼罩','黑丝','JK','OL','cos','制服','学生','汉服','女警','兔女郎']:
            return 'uniform'

        if tag in ['约啪','妻子','伦理','女友','偷情']:
            return 'relation'

        if tag in ['手交','迷奸','器具','乱交','骑乘','乳交','肛交','后入','调教','双飞','女女','足交','多P','口交','自慰']:

            return 'mating'

        if tag in ['颜射','口爆','狂射','内射']:
            return 'ejaculation'

        if tag in ['美胸','KTV','户外','表情','淫叫','露出','呻吟','媚','贫乳','丰满','嘴','巨乳','野外','车上','骨感','长发','内窥','孕妇','美臀','高挑','短发','身材','大屌','对白','无毛','处女','美穴','特别','美足','美乳','美腿','公共场所','电话','黑白']:
            return 'outstanding'
        return 'tag'

if __name__ == "__main__":
    workDir=r"E:\avideo"
    tm=TagManager(workDir)
    cmd=sys.argv[1]
    if cmd=="1":
        tm.Export()
    if cmd=="2":
        tm.Import()