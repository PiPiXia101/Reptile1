from urllib import request
#链接头信息池
from useragents import ua_list
#mysql工具包
from conn import Mysql_

import re
import random
import csv
import time



class MaoYan:
    def __init__(self):
        self.url = 'https://maoyan.com/board/4?offset={}'

    def get_html(self, url):
        headers = {
            'User-Agent': random.choice(ua_list)
        }
        req = request.Request(url=url, headers=headers)
        res = request.urlopen(req)
        html = res.read().decode('utf-8')
        return html

    def parse_html(self, html):
        p = re.compile(
            '<div class="movie-item-info">.*?title="(.*?)".*?class="star">(.*?)</p>.*?releasetime">(.*?)</p>', re.S)
        result = p.findall(html)
        return result

    def write_page(self, list):
        mysql_ = Mysql_('stu', 'root', '123456')
        sql = 'insert into movie values(%s,%s,%s);'

        r_list = []
        for item in list:
            actor = item[1].strip()
            time = item[2].strip()
            r_tuple = (item[0].strip(), actor[3:], time[5:])
            # print(r_tuple)
            mysql_.add_del_upd(sql, r_tuple)
            r_list.append(r_tuple)
        with open('file.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerows(r_list)





    def main(self):
        for i in range(0,100,10):
            url = self.url.format(i)
            html = self.get_html(url)
            r_list = self.parse_html(html)
            self.write_page(r_list)
            time.sleep(random.randint(2,4))


if __name__ == '__main__':
    MY = MaoYan()
    MY.main()
