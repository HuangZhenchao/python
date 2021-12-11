import time

from selenium import webdriver
from selenium.webdriver.support.select import Select
import html2text
#options.set_headless(True)
h=html2text.HTML2Text()
h.ignore_links=True

class seleniumScrapy:
    def __init__(self):
        pass

    def init(self):
        options = webdriver.FirefoxOptions()
        # options.add_argument("--headless") #设置火狐为headless无界面模式
        # options.add_argument("--disable-gpu")
        # driver=webdriver.Firefox(options=options)

        # 配置文件地址
        profile_directory = r'D:\FirefoxProfile\selenium'
        # 加载配置配置
        profile = webdriver.FirefoxProfile(profile_directory)
        # 启动浏览器配置
        self.driver = webdriver.Firefox(firefox_profile=profile,options=options)#

    def parse_yushuwu(self):
        base_Url='http://www.yushuwu.info'
        driver=self.driver
        driver.get(base_Url+'/1_1171/')
        title=driver.title
        links=driver.find_elements_by_xpath('//dl/dd/a')
        text=''
        urlList=[]
        for link in links:
            print(link.text)
            print(link.get_attribute("href"))
            urlList.append(link.get_attribute("href"))
        for url in urlList:
            driver.get(url)
            contentHtml=driver.find_element_by_id('content').get_attribute('innerHTML')
            text=text+h.handle(contentHtml)
        file_path="D:\\"+title+".txt"
        with open(file_path,'a',encoding='utf-8') as f:
            f.write(text)
        #driver.quit()


print("开始")
seleniumScrapy=seleniumScrapy()
a=time.time()
print(a)
seleniumScrapy.init()
b=time.time()
print(b)
print(b-a)
a=time.time()
seleniumScrapy.parse_sinocal()
b=time.time()
print(b-a)