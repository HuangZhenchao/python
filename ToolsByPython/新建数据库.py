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