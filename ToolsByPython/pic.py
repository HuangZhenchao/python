import os
import shutil


# 遍历文件夹
# 创建sel和del文件夹
# 将每组图片选取第一个到sel文件夹
# 手动将要删除的图片放到del文件夹
# G:\图片2：待归档\jilebox-photo\990
import sys


def sel(dir):
    os.mkdir(dir + "\\sel")
    os.mkdir(dir + "\\del")
    files = os.listdir(dir)
    for file in files:
        if file.find("_1.jpg") > 0:
            file_path = dir + "\\" + file
            file_copy_path = dir + "\\sel\\" + file
            print(file_path)
            print(file_copy_path)
            shutil.copyfile(file_path, file_copy_path)



def delfile(dir):
    low_file_dir = dir + "\\del"
    low_files = os.listdir(low_file_dir)
    print("删除",len(low_files),"组")
    orderList = []
    for low_file in low_files:
        orderNum = low_file.split("_")[0]
        orderList.append(orderNum)
        os.remove(low_file_dir + "\\" + low_file)
    # 遍历图片，一一判断
    all_files = os.listdir(dir)
    for file in all_files:
        orderNum = file.split("_")[0]
        if orderNum in orderList:
            os.remove(dir + "\\" + file)


def delsel(dir):
    low_file_dir = dir + "\\del"
    sel_file_dir = dir + "\\sel"
    shutil.rmtree(low_file_dir)
    shutil.rmtree(sel_file_dir)


if __name__ == "__main__":
    print("开始")
    workdir=r"F:\图片2：待归档\jilebox-photo\829"
    workdir=sys.argv[2]
    if sys.argv[1]=="1":
        sel(workdir)

    if sys.argv[1]=="2":
        delfile(workdir)
        print("完成")
