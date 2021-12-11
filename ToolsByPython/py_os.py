import os
import sys

def check_filename_available(filename):
    n=[0]
    def check_meta(file_name):
        file_name_new=file_name
        if os.path.isfile(file_name):
            file_name_new=file_name[:file_name.rfind('.')]+'_'+str(n[0])+file_name[file_name.rfind('.'):]
            n[0]+=1
        if os.path.isfile(file_name_new):
            file_name_new=check_meta(file_name)
        return file_name_new
    return_name=check_meta(filename)
    return return_name


def fun(dir):
    descriptPath=os.path.join(dir,'descript.ion')
    for file in os.listdir(dir):
        path=os.path.join(dir,file)
        if os.path.isdir(path):
            fun(path)
        ext=file[file.rfind('.'):]
        arr=file[:file.rfind('.')].split(";")
        descript=''
        rename=arr[len(arr)-1]+ext
        newpath=os.path.join(dir,rename)
        newpath=check_filename_available(newpath)
        for int in range(0,len(arr)-1):
            descript=descript+arr[int]+';'
        print(descript)
        print(rename)
        with open(descriptPath,'a') as f:
            f.writelines('\"'+os.path.basename(newpath)+'\"'+' '+descript+'\n')
        os.rename(path,newpath)
def fun1(dir):
    descriptPath=os.path.join(dir,'descript.ion')
    for file in os.listdir(dir):
        path=os.path.join(dir,file)
        if os.path.isdir(path):
            fun(path)
        ext=file[file.rfind('.'):]
        arr=file[:file.rfind('.')].split(";")
        descript=''
        rename=arr[0]+'.'+ext
        newpath=os.path.join(dir,rename)
        newpath=check_filename_available(newpath)
        for int in range(1,len(arr)):
            descript=descript+arr[int]+';'
        print(descript)
        print(rename)
        with open(descriptPath,'a') as f:
            f.writelines('\"'+os.path.basename(newpath)+'\"'+' '+descript+'\n')
        os.rename(path,newpath)

'''
def fun2(dir):
    descriptPath=os.path.join(dir,'descript.ion')

    with open(descriptPath,'r',encoding='gbk') as f:
        for line in f.readlines():
            cursor = db.cursor()
            strFile=line.split(" ")[0]
            path=os.path.join(dir,strFile)
            strRemakes=line.split(" ")[1]
            lRemake=strRemakes.split(";")
            for each in lRemake:
                if each=='\n':
                    continue
                print(each=='\n',path,each)
                cursor.execute(sqlInsertTag,(each,path))
            cursor.execute(sqlInsertFile,(path,strRemakes))
            # 提交到数据库执行
            db.commit()
'''
if __name__ == "__main__":
    cmd="1"
    cmd=sys.argv[1]
    workDir="E:\\000"
    workDir=sys.argv[2]
    if cmd=="1":
        fun(workDir)

    if cmd=="2":
        pass
        # fun2(sys.argv[2])


    #for root, dirs, files in os.walk(wordDir, topdown=False):
     #   for dir in dirs:
      #      fun2(os.path.join(root, dir))
    print(cmd)

    print("完成")
