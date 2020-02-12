# -*- coding: utf-8 -*-
import scrapy
import json
from xianhuo.items import XianhuoItem


class Element14Spider(scrapy.Spider):
    name = 'element14'
    allowed_domains = ['https://cn.element14.com']
    start_urls = ['https://cn.element14.com/search/prl/results?brand=te-connectivity']
    # start_urls = ['https://cn.element14.com/w/search/prl/results?brand=te-connectivity&pageSize=100']

    def parse(self, response):
        # 1. 匹配出所有商品信息的盒子
        altRows = response.css('#sProdList').xpath('tbody/tr')
        # 2. 遍历匹配出信息
        for altRow in altRows:
            item = XianhuoItem()
            # 型号
            item["model"] = altRow.xpath('td[contains(@class,"productImage")]/input[@class="hVal"]/@value').extract_first()
            # 价格
            item["price"] = json.dumps(altRow.xpath('td[@class="listPrice"][2]/div[1]/p//span[@class="qty_price_range"]/text()').re('CNY(.*)'))
            # 价格梯度
            item["levels"] = json.dumps(altRow.xpath('td[@class="listPrice"][2]/div[1]/p//span[@class="qty"]/text()').re("(.*?)\+"))
            # 品牌
            item["brand"] = altRow.xpath('td[@class="description"]/a/p[1]/text()').extract_first()
            item["shop"] = "element14"
            item["status"] = "1"
            yield item

        # 下一页
        next = response.xpath('//span[@class="paginNextArrow"]/a/@href').extract_first()
        yield scrapy.Request(url=next, callback=self.parse, dont_filter=True)

