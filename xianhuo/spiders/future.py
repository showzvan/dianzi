# -*- coding: utf-8 -*-
import scrapy
import json
from xianhuo.items import XianhuoItem


# https://www.futureelectronics.cn/search?q=TE&#x20;Connectivity:relevance:manufacturerName:TE Connectivity&selectedTab=products&text=TE&#x20;Connectivity&pageSize=100&page=1
# https://www.futureelectronics.cn/search?q=TE%20Connectivity:relevance:manufacturerName:TE%20Connectivity&selectedTab=products&text=TE%20Connectivity&pageSize=100
# https://www.futureelectronics.cn/search?q=TE&#x20;Connectivity:relevance:manufacturerName:TE%20Connectivity&selectedTab=products&text=TE&#x20;Connectivity&pageSize=100&page=1
# https://www.futureelectronics.cn/search?q=TE&#x20;Connectivity:relevance:manufacturerName:TE Connectivity&selectedTab=products&text=TE&#x20;Connectivity&pageSize=100&page=1


# 下一次开始
# https://www.futureelectronics.cn/search?q=TE%20Connectivity:relevance:manufacturerName:TE%20Connectivity&selectedTab=products&text=TE%20Connectivity&pageSize=100&page=47



class FutureSpider(scrapy.Spider):
    name = 'future'
    allowed_domains = ['https://www.futureelectronics.cn/']
    start_urls = ['https://www.futureelectronics.cn/search?q=TE%20Connectivity:relevance:manufacturerName:TE%20Connectivity&selectedTab=products&text=TE%20Connectivity&pageSize=100']

    def parse(self, response):
        productsLists = response.xpath('body/main/div//div[@class="product_list_inner"]//tr[@class="list-row"]')
        for i in productsLists:
            item = XianhuoItem()
            # 料号
            item["model"] = i.xpath('th[@class="product__list--item"]//a[@class="product__list--code"]/text()').extract_first()
            # 品牌
            item["brand"] = i.xpath('th[@class="product__list--item"]//div[@class="product__list--name"]/text()').extract_first()
            # 价格
            item["price"] = json.dumps(i.xpath('td[@class="product_price"]//span[@class="product_price_val"]/text()').re("¥(.*?) "))
            # 价格阶梯
            item["levels"] = json.dumps(i.xpath('td[@class="product_price"]//span[@class="product_price_qty"]/text()').re("(.*):"))
            # 商城
            item["shop"] = "future"
            # 状态
            item["status"] = "1"
            yield item
        # 下一页
        next = response.xpath('body/main/div//div[contains(@class,"search-plp")]//li[@class="pagination-next"]/a/@href').extract_first()
        # print(next)
        url = response.urljoin(next.replace(" ","%20").replace("&#x20;","%20"))
        print(url)
        yield scrapy.Request(url=url,callback=self.parse,dont_filter=True)