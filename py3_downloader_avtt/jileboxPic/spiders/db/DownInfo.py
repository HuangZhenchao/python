#! /usr/bin/env python
import sqlite3
from ..globalValue import *
class DownInfo():
    def __init__(self):
        self.db_name =get_global_value('db_name')
        self.FileInfo_tname = get_global_value('FileInfo_tname')
        self.md5Info_tname=get_global_value('md5Info_tname')


    def update_down_info(self,tdata):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        if tdata['state']:
            tempStr = 'state={}'.format(tdata['state'])
        if tdata['ID']:
            whereStr = 'ID={}'.format(tdata['ID'])
        sqlStr = 'UPDATE {} SET {} WHERE {};'.format(self.FileInfo_tname, tempStr, whereStr)
        print(sqlStr)
        c.execute(sqlStr)
        print('更新{}下载状态为{}'.format(tdata['name'], str(tdata['state'])))
        conn.commit()
        conn.close()

    def select_down_info(self,tdata):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        whereStr = ' 1=1'
        if tdata['name'] != '':
            whereStr = whereStr + ' AND name=\'{}\''.format(tdata['name'])
        else:
            whereStr = whereStr + ' AND state=0'
        sqlStr = 'SELECT * FROM {} WHERE {} ORDER BY name DESC limit 20;'.format(self.FileInfo_tname, whereStr)
        print(sqlStr)
        c.execute(sqlStr)
        retItem = c.fetchall()
        conn.commit()
        conn.close()
        return retItem

    def insert_down_info(self,tdata):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        sqlStr = 'INSERT INTO {} (pageID,state,name,folder,url,key) VALUES ({},{},\'{}\',\'{}\',\'{}\',\'{}\');' \
            .format(self.FileInfo_tname, tdata['pageID'], tdata['state'], tdata['name'], tdata['folder'], tdata['url'], tdata['key'])
        print(sqlStr)
        c.execute(sqlStr)
        # retItem = c.fetchall()
        conn.commit()
        conn.close()

    def AddMD5(self,value):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        c.execute('INSERT INTO {} (md5)VALUES (\'{}\');'.format(self.md5Info_tname,value))
        print("插入一条md5")
        conn.commit()
        conn.close()

    def IsMd5Exist(self,value):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('SELECT id FROM {} WHERE md5=\'{}\';'.format(self.md5Info_tname,value))
        ret =c.fetchall()
        conn.commit()
        conn.close()
        if len(ret)==0:
            return False
        else:
            print("MD5已经存在")
            return True
