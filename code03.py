from bs4 import BeautifulSoup
from lxml import html
import xml
import requests

"""
    模拟达内登录,通过分析获得到请求头和请求体里的东西,获取到Cookie的东西
"""


header = {
    "Accept": "*/*",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "http://www.tmooc.cn",
    "Referer": "http://www.tmooc.cn/",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    
}
login_url = "http://uc.tmooc.cn/login"
page = requests.Session()     #用Session发出请求能自动处理Cookie等问题
page.headers = header		 #为所有请求设置头
page.get(login_url)    #Get该地址建立连接(通常GET该网址后，服务器会发送一些用于验证的参数用于识别用户，这些参数在这就全由requests.Session处理了)

From_Data={
    "loginName": "1535943024@qq.com",
    "password": "3b479c06bd4c588bb2539440cda9b6a9",
    "imgCode": "",
    "accountType": "1",
}

q = page.post(login_url,data=From_Data,headers=header) 
print(q.url)	#这句可以查看请求的URL
print(q.status_code)  #这句可以查看请求状态
for (i,j) in q.headers.items():
    print(i,':',j)		#这里可以查看响应头
print('\n\n')
for (i,j) in q.request.headers.items():
    print(i,':',j)		#这里可以查看请求头