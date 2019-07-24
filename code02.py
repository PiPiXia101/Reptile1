import time
import random
import re
import requests
from urllib import parse

def parse_page(url, t):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'Connection': 'close'
    }
    time.sleep(random.randint(1, 5))
    response = requests.get(url, headers)
    print("第" + str(t) + "章请求正常")
    # 网站的格式是gbk格式
    text = response.content.decode('gbk') 
    # 这里是获取小说正文部分的正则表达式
    base_content = re.findall(r'<div class="text"\salign="justify">.*?<p>(.*?)</p>', text, re.DOTALL)
    print("第" + str(t) + "章解析正常")
    # 这里是获取小说的章节名称
    page_name = re.findall(r'<div id="Article">.*?<h1>(.*?)<br>', text, re.DOTALL)
    # 这里是获取小说的下一章节的网址
    next_page = re.findall(r'<p align="center">.*?<a href=.*?>.*?</a>.*?<a href=.*?>.*?</a>.*?<a href=(.*?)>.*?</a>', text, re.DOTALL)[1]
    for content in base_content:
        x = re.sub(r'<p>', "", content)
        p = re.sub(r'&nbsp;|\n', "", x)
        # 这里采用追加的方式写入
        with open("code02/"+str(t)+".txt", 'a', encoding='utf-8') as fp:
        	# 这里是去除空格和换行符 
            p = p.strip()
            fp.write(str(page_name) + "\n" + '='*100 + "\n")
            fp.write(p + "\n" + "="*100 + "\n")
        print("第" + str(t) + "章写入文件正常")
    print("第" + str(t) + "章抓取正常")
    next_page = next_page.replace('\'', '')
    # 这里是返回下一章节的网址，方便爬取
    return next_page

def main():
    original_url = "https://www.kanunu8.com/book2/10943/194884.html"
    base_url1 = "https://www.kanunu8.com/"
    base_url2 = "book2/10943/"
    next_page_url_1 = parse_page(original_url, 1)
    real_url = original_url
    for t in range(2, 180):
        next_page_url_2 = base_url2 + next_page_url_1
        real_url = parse.urljoin(base_url1, next_page_url_2)
        print('Url打印正确: ' + real_url)
        next_page_url_1 = parse_page(real_url, t)
        if next_page_url_1 == './':
            break
            print("已经全部爬取完，结束爬取")


if __name__ == '__main__':
    main()
