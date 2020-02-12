# -*- coding: utf-8 -*-
import scrapy

""""
1. 改写 start_requests 函数
2. 计算总页数，循环爬取
3. 解析json，提取数据
4. 与items字段绑定

2020-02-12 问题：
    asdfghjkl 生成的方式还未找到
"""

class LiexinSpider(scrapy.Spider):
    name = 'liexin'
    allowed_domains = ['https://www.ichunt.com/']
    start_urls = ['https://www.ichunt.com/s/?k=TE(%E6%B3%B0%E7%A7%91)&stag=liexin&search_type=1']
    # qwertyuiop - > 时间戳
    # asdfghjkl - >
    data = {
        "goods_name/condition": "TE(泰科)",
        "com_rank": "1",
        "p": "1",
        "offset": "5",
        "pf": "1",
        "qwertyuiop": "",
        "asdfghjkl": "7455dcc2d0c119d89cc0044871ee15cbcddc8fe1",
    }

    def start_requests(self):


    def parse(self, response):
        goodsBox = response.css('.self-search .self-box')
        print(goodsBox)
