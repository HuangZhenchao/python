#! /usr/bin/env python
import sqlite3
class tTsVideo_avtt():
    db_name = 'D:\\DownInfo.db'
    tname = 'tTsVideoInfo_avtt'
    def __init__(self,path):
        pass
        #self.db_name = 'D:\\DownInfo.db'
        #self.tname = 'tTsVideo_avtt'

    @classmethod
    def update_down_info(cls,tdata):
        conn = sqlite3.connect(cls.db_name)
        c = conn.cursor()
        if tdata['state']:
            tempStr = 'state={}'.format(tdata['state'])
        if tdata['ID']:
            whereStr = 'ID={}'.format(tdata['ID'])
        sqlStr = 'UPDATE {} SET {} WHERE {};'.format(cls.tname, tempStr, whereStr)
        print(sqlStr)
        c.execute(sqlStr)
        print('更新{}下载状态为{}'.format(tdata['name'], str(tdata['state'])))
        conn.commit()
        conn.close()

    @classmethod
    def select_down_info(cls,tdata):
        conn = sqlite3.connect(cls.db_name)
        c = conn.cursor()
        whereStr = ' 1=1'
        if tdata['name'] != '':
            whereStr = whereStr + ' AND name=\'{}\''.format(tdata['name'])
        else:
            whereStr = whereStr + ' AND state=0'
        sqlStr = 'SELECT * FROM {} WHERE {} ORDER BY name DESC limit 20;'.format(cls.tname, whereStr)
        print(sqlStr)
        c.execute(sqlStr)
        retItem = c.fetchall()
        conn.commit()
        conn.close()
        return retItem

    @classmethod
    def insert_down_info(cls,tdata):
        conn = sqlite3.connect(cls.db_name)
        c = conn.cursor()
        sqlStr = 'INSERT INTO {} (pageID,state,name,folder,url,key) VALUES ({},{},\'{}\',\'{}\',\'{}\',\'{}\');' \
            .format(cls.tname, tdata['pageID'], tdata['state'], tdata['name'], tdata['folder'], tdata['url'], tdata['key'])
        print(sqlStr)
        c.execute(sqlStr)
        # retItem = c.fetchall()
        conn.commit()
        conn.close()

