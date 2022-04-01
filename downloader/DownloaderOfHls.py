from req import req
from Crypto.Cipher import AES  # Crypto   #PyCryptodome
from concurrent.futures import ThreadPoolExecutor

url=''
resp=req(url)
if resp:
    with open(file_path, 'wb') as f:
        f.write(resp.content)

class DownloaderOfHls:
    def __init__(self):
        with ThreadPoolExecutor(5) as executor:
            for i in range(start_page, end_page):
                executor.submit(self.SiteParser, i)
        pass

    def parseM3U8(self):
        #5.获取并解析m3u8文件
        res_m3u8=req(m3u8_url)
        # 事先查看m3u8文件，只是一些信息，不是包含ts文件列表的m3u8
        # 替换地址，继续获取
        if not res_m3u8:
            continue
        #print m3u8_url
        #print(re.findall('\n(.*?)index.m3u8',res_m3u8.content.decode('utf-8'))[0]+'index.m3u8')
        substr2=re.findall('\n(.*?)index.m3u8',res_m3u8.content.decode('utf-8'))[0]+'index.m3u8'
        print(substr2)
        m3u8_url_final=re.sub('index.m3u8',substr2,m3u8_url)
        print(substr2)
        print(m3u8_url_final)
        res_m3u8_final=req(m3u8_url_final)
        if not res_m3u8_final:
            continue

        #avtt里的m3u8是有key.key的
        #获取key文件
        key_url=re.sub('index.m3u8', 'key.key', m3u8_url_final)
        print(key_url)
        res_key=req(key_url)
        if not res_key:
            continue

        key=res_key.text
        print(key)
        #获取到ts文件列表
        pattern1 = re.compile(r",(.*?)#")
        tslist = pattern1.findall(re.sub('\n', '', res_m3u8_final.content.decode('utf-8')))
        index=0
        for ts in tslist:
            if not 'ts' in ts:
                continue

    def downTs(self):
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

