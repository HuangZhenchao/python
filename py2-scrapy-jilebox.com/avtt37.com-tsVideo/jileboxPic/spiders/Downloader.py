#! /usr/bin/env python
import os
import re
import threading

from Crypto.Cipher import AES  # Crypto   #PyCryptodome

from .db.tTsVideo_avtt import tTsVideo_avtt
from .req import req

lock=threading.Lock()

class CDownload ():   # 继承父类threading.Thread
    def __init__(self,save_path):
        self.save_path=save_path


    def download(self,down_info):

        path=self.save_path+down_info['folder']+'/'
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
            '''
            if os.path.exists(self.video_md5_file):
                md5 = hashlib.md5()
                for chunk in resp.iter_content(chunk_size=1024):
                    if chunk:
                        md5.update(chunk)
                md5str = md5.hexdigest()
                print md5str
                state = 2
                if not IsMd5Exist(self.video_md5_file,md5str):
                    AddMD5(self.video_md5_file,md5str)
            '''
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
            tTsVideo_avtt.update_down_info(tdata)
