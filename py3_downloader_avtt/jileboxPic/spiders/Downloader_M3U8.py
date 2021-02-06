#! /usr/bin/env python
import sqlite3
import re
import shutil,os
import hashlib
import subprocess
import queue
from .globalValue import *
from .req import req
from threading import Thread
from Crypto.Cipher import AES  # Crypto   #PyCryptodome
class Downloader_M3U8():
    def __init__(self,db_name,ts_table_name,m3u8_table_name):
        self.db_name=db_name
        self.q_CompletionDegree=queue.Queue()
        self.q_down = queue.Queue()
        self.ts_table_name = ts_table_name
        self.m3u8_table_name = m3u8_table_name

    def Down(self):
        all_task_done=False
        # ContentPageUrl,ResourceType,ResourceUrl,ResourceDetail,TaskStart,ChildTaskTotal,ChildTaskTotalList,ChildTaskDone,ChildTaskDoneList,TaskDone
        while True:
            if all_task_done:
                break
            #上一个任务已完成，从数据库中取出一个任务

            db_name = 'D:/DownInfo.db'

            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            sqlStr = 'SELECT * FROM {} WHERE TaskDone=0 ORDER BY id DESC limit 1;'.format(self.m3u8_table_name)
            print(sqlStr)
            c.execute(sqlStr)
            returnItem = c.fetchall()
            if len(returnItem)==0:
                all_task_done=True
                break
            retItem=returnItem[0]

            c = conn.cursor()
            sqlStr = 'SELECT * FROM {} WHERE DetailPageUrl=\'{}\' ORDER BY id;'.format(self.ts_table_name,retItem[1])
            print(sqlStr)
            c.execute(sqlStr)
            retItem1 = c.fetchall()

            c = conn.cursor()
            sqlStr = 'SELECT * FROM {} WHERE DetailPageUrl=\'{}\' AND state=0 ORDER BY id;'.format(self.ts_table_name,retItem[1])
            print(sqlStr)
            c.execute(sqlStr)
            retItem2 = c.fetchall()

            conn.commit()
            conn.close()


            #获取一些下载信息，如保存位置，存放目录
            str=re.sub('http://','',retItem[1])
            str = re.sub('http://', '', str)
            #看有没有子任务
            #以/分割URL，最后一部分取做文件名，中间以_连接，作为目录
            list=str.split('/')
            filename=list[len(list)-1]+'#'+retItem[5]
            filename=re.sub('\?', ' ', filename)
            del(list[-1])
            path_str=''
            for each in list:
                if path_str=='':
                    path_str+=each
                else:
                    path_str += '_'+each
            task_file_dir=get_global_value('file_save_path')+path_str+'\\'

            child_task_file_dir=task_file_dir+filename+'\\'
            if not os.path.exists(child_task_file_dir):
                os.makedirs(child_task_file_dir)
            task_listfile_path=child_task_file_dir+'tslist.txt'
            task_file_path=task_file_dir+filename+'.mp4'
            print(child_task_file_dir)
            # 从数据库读取下载任务到队列
            file_str=''
            for data in retItem1:
                file_str = file_str + 'file \'{}\'\n'.format(os.path.join(child_task_file_dir, data[2]))
            with open(task_listfile_path, 'w') as f:
                f.write(file_str)

            # 开启多线程下载
            for j in range(5):  # 新建5个线程 等待队列
                t3 = Thread(target=self.TChildTaskDownload)
                #t3.setDaemon(True)
                t3.start()

            merge_flag=0
            for task in retItem2:

                q_down_data={
                    'retItem':retItem,
                    'file_path':os.path.join(child_task_file_dir, task[2]),
                    'task_url':task[3],
                    'key':retItem[10]
                }

                self.q_down.put(q_down_data)
            #添加线程结束标志
            for i in range(5):
                self.q_down.put(None)
            #使线程阻塞，直至下载任务完成
            self.q_down.join()

            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            sqlStr = 'UPDATE {} SET  TaskDone=1 WHERE id={};'.format(self.m3u8_table_name,retItem[0])
            print(sqlStr)
            c.execute(sqlStr)
            conn.commit()
            conn.close()


    def TChildTaskDownload(self):
        while True:
            print('执行 下载线程')
            q_down_data = self.q_down.get()

            if q_down_data==None:
                self.q_down.task_done()
                break
            print(q_down_data['task_url'])

            if not os.path.exists(q_down_data['file_path']):
                resp = req(q_down_data['task_url'])
                if resp:
                    # continue

                    with open(q_down_data['file_path'], 'wb') as f:
                        if len(q_down_data['key']):  # AES 解密
                            cryptor = AES.new(q_down_data['key'].encode('utf-8'), AES.MODE_CBC)
                            f.write(cryptor.decrypt(resp.content))
                        else:
                            f.write(resp.content)
                    conn = sqlite3.connect(self.db_name)
                    c = conn.cursor()
                    sqlStr = 'UPDATE {} SET  state=1 WHERE ts_uri=\'{}\';'.format(self.ts_table_name, q_down_data['task_url'])
                    print(sqlStr)
                    c.execute(sqlStr)
                    c = conn.cursor()
                    sqlStr = 'UPDATE {} SET  ChildTaskDone=ChildTaskDone+1 WHERE id={};'.format(self.m3u8_table_name, q_down_data['retItem'][0])
                    print(sqlStr)
                    c.execute(sqlStr)
                    conn.commit()
                    conn.close()
            self.q_down.task_done()
            

