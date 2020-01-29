# -*- coding: utf-8 -*-
import scrapy
import re
import requests
import json
from scrapy import Selector
from xianhuo.items import XianhuoItem


class YingzhichengSpider(scrapy.Spider):
    name = 'yingzhicheng'
    allowed_domains = ['https://www.allchips.com/']
    start_urls = ['https://www.allchips.com/search?key=%E6%B3%B0%E7%A7%91&brand=210']
    url = "https://www.allchips.com/website/api/ware/search/searchWareList"
    typeList = ["40","20"]
    totalPage = 1
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        # "content-length": "50",
        "content-type": "application/json",
        # "cookie": '',
        "csrftoken": "1",
        "origin": "https://www.allchips.com",
        "referer": "https://www.allchips.com/search?key=%E6%B3%B0%E7%A7%91&brand=210",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }
    data = {
        "pageSize": "10",
        "pageNo": "",
        "searchType": "20",
        "keyword": "泰科",
        "deliveryMin": "0",
        "brand": "210",
        "displayareaCode": "",
    }
    nu = 1
    #
    # def start_requests(self):
    #     url = 'https://www.allchips.com/search?key=%E6%B3%B0%E7%A7%91&brand=210'
    #     response = requests.get(url = url, headers=self.headers)
    #     yield response
    #


    def parse(self, response):
        # 获取csrftoken
        csrf = response.xpath('//head').re_first("csrfToken = '(.*?)'")
        # csrf = re.search("csrfToken = '(.*?)'", response.text, re.S)
        self.headers['csrftoken'] = csrf
        # print(self.headers['csrftoken'])
        # 设置cookie
        # cookie = requests.utils.dict_from_cookiejar(response.cookies)
        # 获取自营总页数
        # response = Selector(text=response.text)
        totalPageZy = response.xpath(
            '//div[contains(@class,"ft")]/span/a[@data-displayareacode="40"]/@data-totalpagecount').extract_first()
        # 获取代售总页数
        totalPageDc = response.xpath(
            '//div[contains(@class,"ft")]/span/a[@data-displayareacode="20"]/@data-totalpagecount').extract_first()
        # print("自营页数：%s,代售页数：%s" % (totalPageZy, totalPageDc))
        for i in self.typeList:
            self.data["displayareaCode"] = i
            if i == "40":
                self.totalPage = totalPageZy
            else:
                self.totalPage = totalPageDc
            for j in range(1, int(self.totalPage) + 1):
                self.data["displayareaCode"] = i
                print("这是data：%s" % self.data["displayareaCode"])
                print("这是总页数%s" % self.totalPage)
                # for j in range(1, 2):
                print(type(j))
                # print(self.totalPage)
                # print(self.data)
                # self.data["pageNo"] = str(j)
                self.data.update({"pageNo": str(j)})
                # print(j)
                data = json.dumps(self.data)
                # 发送post请求接口数据
                # print(j)
                yield scrapy.Request(url=self.url, method="POST", body=data, headers=self.headers, callback=self.dl_resault,
                                     dont_filter=True)

    def dl_resault(self,response):
        n = json.loads(response.text)
        a = n["data"]["result"]
        print(n["data"]["currentPageNo"])
        # print(type(a))
        for i in a:
            item = XianhuoItem()
            item["model"] = i["wareType"]["partNumber"]
            item["price"] = json.dumps([p["priceCN"] for p in i["prices"]])
            item["levels"] = json.dumps([p["minAmount"] for p in i["prices"]])
            item["brand"] = i["wareType"]["brandName"]
            item["shop"] = "硬之城"
            item["status"] = "1"
            item["page"] = n["data"]["currentPageNo"]
            yield item
        # # yield self.parse

        # n = json.loads(response.text)
        # a = n["data"]["result"]
        # print(n["data"]["currentPageNo"])
        # # print(type(a))
        # for i in a:
        #     item = XianhuoItem()
        #     item["model"] = i["wareType"]["partNumber"]
        #     item["price"] = json.dumps([p["priceCN"] for p in i["prices"]])
        #     item["levels"] = json.dumps([p["minAmount"] for p in i["prices"]])
        #     item["brand"] = i["wareType"]["brandName"]
        #     item["shop"] = "硬之城"
        #     item["status"] = "1"
        #     item["page"] = n["data"]["currentPageNo"]
        #     yield item
        # # yield self.parse

    #     """
    #     1. 通过请求 数据接口 把需要的json数据获取到   json.loads(response.body)  注意：需要把header，data都配好，通过post请求
    #     2. 进行数据的匹配 提取需要的数据   料号、价格   使用json.loads/dumps 或者 re 的方法进行匹配
    #     3. 匹配好的数据 存入item 放入数据库
    #     4. 分页：根据得到的 json，post发送不同的页码以请求不同数据
    #     问题：需要得到 自营 和 代售 两部分数据 怎么弄？   在post数据中 displayareaCode 不同，自营是 40， 代售是 20 以此区分
    #     :param response:
    #     :return:
    #     """
    #     # 获取csrftoken
    #     csrf = re.search("csrfToken = '(.*?)'",response.text,re.S)
    #     self.headers['csrftoken'] = csrf[1]
    #     # 获取自营总页数
    #     totalPageZy = response.xpath('//div[contains(@class,"ft")]/span/a[@data-displayareacode="40"]/@data-totalpagecount').extract_first()
    #     # 获取代售总页数
    #     totalPageDc = response.xpath('//div[contains(@class,"ft")]/span/a[@data-displayareacode="20"]/@data-totalpagecount').extract_first()
    #
    #     print("自营页数：%s,代售页数：%s" %(totalPageZy,totalPageDc))
    #
    #
    #     for i in self.typeList:
    #         self.data["displayareaCode"] = i
    #         if i == "20":
    #             self.totalPage = totalPageZy
    #         else:
    #             self.totalPage = totalPageDc
    #         for j in range(1,int(self.totalPage) + 1):
    #             self.data["pageNo"] = str(j)
    #             # 发送post请求接口数据
    #             a = scrapy.FormRequest(method='POST',url=self.url,formdata=self.data)
    #             print(json.loads(a))
    #             break



        # listTabs = response.css(".jsListTabBox") # selectorList
        # for listTab in listTabs:
        #     wares = listTab.css('.ware-content-tr')
        #     for ware in wares:
        #         item = XianhuoItem()
        #         # 型号
        #         # item["model"] = ware.xpath('div[contains(@class,"search-content-td")]/div[@class="table-cell"]/div[contains(@class,"partnum")]/a[contains(@class,"part")]/text()').extract_first()
        #         # 价格
        #         # 价格梯度
        #         # 品牌
        #         # 商城名
        #         # yield item
        #
        #     # 翻页页码
        #     next = wares.xpath('//a[contains(@class,"jsLoadMore")]/@data-pageno').extract_first()
        #     print(next)