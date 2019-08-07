from urllib import request,parse
import re
'''
    抓取虎牙英雄联盟区的主播人气排行
'''
class HuYaSpider():
    url = 'https://www.huya.com/g/lol'
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    #使用非贪婪模式，表示匹配到第一个</span>停止
    #一级提取
    pattern_first = '<span class="txt">([\s\S]*?)</span>\n</li>'
    #二级提取:主播名字和主播人气
    pattern_name = '<i class="nick" title="([\s\S]*?)">'
    pattern_popularity = '<i class="js-num">([\s\S]*?)</i></span>'

    #爬取虎牙网页的html信息
    def __crawl_web_html(self):
        req = request.Request(HuYaSpider.url,headers=HuYaSpider.headers)
        htmls = request.urlopen(req).read().decode()
        return htmls
    
    #分析htmls，提取数据
    def __extract_data(self,htmls):
        htmls_first = re.findall(HuYaSpider.pattern_first,htmls)
        list_anchors = []
        for html in htmls_first:
            anchor_name = re.findall(HuYaSpider.pattern_name,html)
            anchor_popularity = re.findall(HuYaSpider.pattern_popularity,html)
            tup = (anchor_name[0],anchor_popularity[0])
            list_anchors.append(tup)
        return list_anchors
    
    #数据排序
    def __reorder(self,anchors):
        #def sorted(iterable, key, reverse)
        #iterable:可迭代对象
        #key：进行比较的元素
        #reverse：默认False，为升序排列;True为降序排列
        anchors = sorted(anchors,key=self.__data_process,reverse=True)
        return anchors
    
    #sorted会将iterable中的每一个元素传入__data_process中，通过其返回的值进行比较
    def __data_process(self,anchor):
        number = re.findall('[\d.]*',anchor[1])
        number = float(number[0])
        if '万' in anchor[1]:
            number *= 10000
        return number

    #主播排名打印   
    def __anchors_rank(self,anchors):
        for anchor in anchors:
            print('主播"'+anchor[0]+'"人气:'+anchor[1])

    #对象的入口方法
    def start(self):
        htmls = self.__crawl_web_html()
        list_anchors = self.__extract_data(htmls)
        anchors = self.__reorder(list_anchors)
        self.__anchors_rank(anchors)
        
lol = HuYaSpider()
lol.start()
