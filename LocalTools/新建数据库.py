#! /usr/bin/env python  
# -*- coding:utf-8 -*-

import sqlite3

conn = sqlite3.connect('D:\\videoID.db')
print "Opened database successfully";
c = conn.cursor()
c.execute('''CREATE TABLE tVideoID
       (ID INTEGER PRIMARY KEY    NOT NULL,      
       videoID INT NOT NULL,
       state  INT NOT NULL DEFAULT 0,
       md5           TEXT    NOT NULL);''')

#page INT NOT NULL,
#state  TEXT NOT NULL
print "Table created successfully";
conn.commit()
conn.close()


# 打开数据库连接
db = pymysql.connect(host="localhost",
                     user="www",
                     password="954325",
                     port=3306,# 端口
                     database="db_tagManager",
                     charset='utf8')
sqlInsertFile="INSERT INTO t_file(filePath,tags)VALUES (%s,%s)"
sqlInsertTag="INSERT INTO t_tag(tag,filePath)VALUES (%s,%s)"
def createTabele():
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # 如果数据表已经存在使用 execute() 方法删除表。
    cursor.execute("DROP TABLE IF EXISTS t_file")

    # 创建数据表SQL语句
    sql = """CREATE TABLE t_file (
             filePath  CHAR(255) NOT NULL,
             tags  CHAR(50))"""
    cursor.execute(sql)

    # 如果数据表已经存在使用 execute() 方法删除表。
    cursor.execute("DROP TABLE IF EXISTS t_tag")
    sql = """CREATE TABLE t_tag (
             tag  CHAR(50) NOT NULL,
             filePath  CHAR(255) NOT NULL)"""
    cursor.execute(sql)

# 关闭数据库连接
db.close()