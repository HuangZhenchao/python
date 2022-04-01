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
        sqlSetectDirs='select winpath from t_video_copy1 GROUP BY winpath;'
        sqlSelectFile='''select a.*,b.tagGroups,b.tags from t_video_copy1 a,(select file,GROUP_CONCAT(tagGroup SEPARATOR ';') as tagGroups,GROUP_CONCAT(tag SEPARATOR ';') as tags from t_videotag_copy1 GROUP BY file) b where a.file=b.file and a.winpath=%s'''
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
                file=result[0]
                #title=result[3]
                tagGroups=result[4].split(";")
                tags=result[5].split(";")
                #oDescription='%s:%s*'%('title',title)
                oDescription=''
                for index,tagGroup in enumerate(tagGroups):
                    oDescription=oDescription+'%s:%s*'%(tagGroup,tags[index])
                f_w.write(file+' '+oDescription+'\n')
        if os.path.exists(ionPath):
            os.remove(ionPath)
        os.rename(tmpIonPath,ionPath)

    def createTable(self):
        self.cursor.execute("DROP TABLE IF EXISTS t_video")
        sqlCreate_t_video="""CREATE TABLE t_video(
                            file varchar(255),
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
        sql="insert into t_video values (%s,%s,%s);"
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

    def Traverse(self,dir):
        ionPath=os.path.join(dir, 'descript.ion')
        if os.path.exists(ionPath):
            with open(ionPath, 'r', encoding='gbk',errors='ignore') as f_read:
                for line in f_read.readlines():
                    # print(workDir,line)
                    listSplite = line.split(" ")
                    #分割备注，获取文件名
                    file=listSplite[0]
                    strTags=listSplite[1].replace('\n','')
                    winPath=dir+'\\'+file
                    projectPath="E:\\node_man"
                    serPath=winPath.replace(projectPath,'').replace('\\','/')
                    self.listFile.append((file,dir,serPath))

                    lTags=strTags.split("*")
                    for tag in lTags:
                        if tag=='':
                            continue
                        pos=tag.find(':')
                        tagGroup=tag[:pos]
                        tagValue=tag[(pos+1):]
                        self.listTag.append((file,tagGroup,tagValue))
        for file in os.listdir(dir):
            path=os.path.join(dir,file)
            if os.path.isdir(path):
                self.Traverse(path)


if __name__ == "__main__":
    workDir='E:\\node_man\\video'
    tm=TagManager(workDir)
    cmd=sys.argv[1]
    if cmd=="1":
        tm.Export()
    if cmd=="2":
        tm.Import()