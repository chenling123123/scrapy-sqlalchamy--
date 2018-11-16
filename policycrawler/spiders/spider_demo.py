import scrapy
from scrapy.selector import Selector
from bs4 import BeautifulSoup
from policycrawler.items import PolicycrawlerItemMiddle,PolicycrawlerItemLast
from scrapy.http import Request
import time
from policycrawler.mongodb_job import CMongo
from policycrawler.model import Policy_Table_Url
from policycrawler.MethodWarehouse import MethodWarehouse
import uuid

class PolicySpider(scrapy.Spider):
    name="policySpider"
    start_urls=[]
    first_url='http://www.chinasei.com.cn/swcy/swyy/index.html'
    start_url='http://www.chinasei.com.cn/swcy/swyy/index_'
    last_url='.html'
    ISOTIMEFORMAT = '%Y-%m-%d %X'

    def __init__(self,current_task_id):
        #调度平台传递的参数
        self.current_task_id = current_task_id
        #self.task_id = task_id
        self.mongo=CMongo()
        self.policy_Table_Url=Policy_Table_Url()
        self.method=MethodWarehouse()
        self.front_name=self.method.read_config("CHILDNODE","0")
        self.front_id=self.method.read_config("CHILDNODE","1")
    def start_requests(self):

        self.start_urls.append(self.first_url)
        for i in range(2):
            self.start_urls.append(self.start_url+str(i)+self.last_url)
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse)


    def parse(self, response):
        selector = Selector(response)

        text0 = selector.xpath('/html/body/div[5]/div[2]/ul').extract_first()
        if text0:
            soup = BeautifulSoup(text0, "lxml")
            if soup.find_all('li'):
                a_s = soup.find_all('li')
                item=PolicycrawlerItemMiddle()
                for li in a_s:
                    if li.find('a'):
                        a = li.find('a')
                        title=a.text
                        mid_url=a.get('href')[1:]
                        if mid_url[0:2]=='./':
                            item['state']=2
                        else:
                            item['state']=0
                        item['url']="http://www.chinasei.com.cn/swcy/swyy"+mid_url
                        item['title']=title
                        #mongoDB中间表数据去重
                        # if self.mongo.get_one("policy_data_mid",item['url']):
                        #     print("该数据已经采集")
                        if self.policy_Table_Url.sele_by_url(item['url']):
                            print("该数据已经采集或网站结构异常"+item['url'])
                        else:
                            yield item
                            yield Request(url="http://www.chinasei.com.cn/swcy/swyy"+mid_url, meta={"url":mid_url,"title":title},callback=self.parse_last)


    def parse_last(self,response):
        selector = Selector(response)
        item=PolicycrawlerItemLast()
        item['url'] = "http://www.chinasei.com.cn/swcy/swyy"+response.meta["url"]
        item['title'] = response.meta["title"]
        text0 = selector.xpath('/html/body/div[5]/div[3]/div[3]/div[1]/div').extract_first()
        item['content']=text0
        pubTime=BeautifulSoup(selector.xpath('/html/body/div[5]/div[3]/div[2]/div[1]').extract_first(), "lxml").text
        if len(pubTime) ==10:
            item['pub_time'] = pubTime+" 00:00:00"
        elif len(pubTime) ==16:
            item['pub_time'] = pubTime + ":00"
        else:
            item['pub_time']=pubTime

        pickTime=str(time.strftime(self.ISOTIMEFORMAT, time.localtime()) )

        item['pick_time']=pickTime
        item['img_path']=''
        item['attachment_path']=''
        item['current_task_id']=self.current_task_id
        method=MethodWarehouse()
        item['id']=str(method.uuid()).replace('-','')
        item['front_name']=self.front_name
        item['front_id']=self.front_id
        #item['modified']=none
        yield item
