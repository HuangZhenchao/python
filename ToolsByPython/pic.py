import os
import shutil


# 遍历文件夹
# 创建sel和del文件夹
# 将每组图片选取第一个到sel文件夹
# 手动将要删除的图片放到del文件夹
# G:\图片2：待归档\jilebox-photo\990
def sel(dir):
    os.mkdir(dir + "\\sel")
    os.mkdir(dir + "\\del")
    files = os.listdir(dir)
    for file in files:
        if file.find("_1") > 0:
            file_path = dir + "\\" + file
            file_copy_path = dir + "\\sel\\" + file
            print(file_path)
            print(file_copy_path)
            shutil.copyfile(file_path, file_copy_path)



def delfile(dir):
    low_file_dir = dir + "\\del"
    low_files = os.listdir(low_file_dir)
    orderList = []
    for low_file in low_files:
        orderNum = low_file.split("_")[0]
        orderList.append(orderNum)
    all_files = os.listdir(dir)
    for file in all_files:
        orderNum = file.split("_")[0]
        if orderNum in orderList:
            print(dir + "\\" + file)
            os.remove(dir + "\\" + file)


if __name__ == "__main__":
    target_dir = "G:\\图片2：待归档\\jilebox-photo"
    # child_dir = "G:\\图片2：待归档\\jilebox-photo\\989"
    folders = os.listdir(target_dir)

    for folder in folders:
        child_dir=target_dir+"\\"+folder
        sel(child_dir)

        # delfile(child_dir)
