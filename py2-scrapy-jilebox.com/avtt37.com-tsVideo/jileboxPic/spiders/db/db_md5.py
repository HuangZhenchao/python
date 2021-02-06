#! /usr/bin/env python
import sqlite3
class CDB_MD5():
    def __init__(self,path):
        self.db_name = 'D:\\md5.db'
        self.tname = ''

    def AddMD5(self,value):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('INSERT INTO file_md5 (md5)VALUES (\''+value+'\');')
        print("插入一条md5")
        conn.commit()
        conn.close()

    def IsMd5Exist(self,value):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('SELECT id FROM file_md5 WHERE md5=\'' + value + '\';')
        ret =c.fetchall()
        conn.commit()
        conn.close()
        if len(ret)==0:
            return False
        else:
            print("MD5已经存在")
            return True