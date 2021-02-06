#! /usr/bin/env python
import os
import re
import threading
import hashlib
from Crypto.Cipher import AES  # Crypto   #PyCryptodome
from .globalValue import *
from .db.DownInfo import DownInfo
from .req import req
from .globalValue import *
lock=threading.Lock()

class CDownload ():   # 继承父类threading.Thread
    def __init__(self):
        self.file_save_path=get_global_value('file_save_path')


    def download(self,down_info):

        path=self.file_save_path+down_info['folder']+'/'
        path=re.sub('\?',' ',path)
        global lock
        lock.acquire()
        try:
            if not os.path.exists(path):
                os.makedirs(path)
        finally:
            lock.release()

        file_path=path+down_info['name']

        resp = req(down_info['url'])
        if resp:
            #continue
            state = 0

            #md5Info_tname不为空时需要校验文件md5,如果文件已存在，state=2
            if get_global_value('md5Info_tname')!='':
                md5 = hashlib.md5()
                for chunk in resp.iter_content(chunk_size=1024):
                    if chunk:
                        md5.update(chunk)
                md5str = md5.hexdigest()
                print(md5str)
                state = 2
                db=get_global_value('db')
                if not db.IsMd5Exist(md5str):
                    db.AddMD5(md5str)
                    state = 0

            if state==0:
                with open(file_path, 'wb') as f:
                    if len(down_info['key']):  # AES 解密
                        cryptor = AES.new(down_info['key'].encode('utf-8'), AES.MODE_CBC)
                        f.write(cryptor.decrypt(resp.content))
                    else:
                        f.write(resp.content)
                state = 1
            tdata={
                'state':state,
                'ID':down_info['ID'],
                'name':down_info['name']
            }
            # TODO:使用数据库
            db = get_global_value('db')
            db.update_down_info(tdata)
