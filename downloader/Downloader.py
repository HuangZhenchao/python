from pylib.net import req
from concurrent.futures import ThreadPoolExecutor

url=''


class Downloader:
    def __init__(self):
        with ThreadPoolExecutor(5) as executor:
            for i in range(start_page, end_page):
                executor.submit(self.SiteParser, i)
        pass

    def down(self):
        resp=req(url)
        if resp:
            with open(file_path, 'wb') as f:
                f.write(resp.content)


