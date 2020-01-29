# -*- coding: utf-8 -*-
import scrapy
import json
from xianhuo.items import XianhuoItem

class PaimingSpider(scrapy.Spider):
    name = 'paiming'
    allowed_domains = ['https://www.iczoom.com/']
    start_urls = ['https://www.iczoom.com/brand/503-c-1-500.html']
    # 下次爬取 12页 开始

    def parse(self, response):
        items = response.css('.product-sell .items-box')
        for i in items:
            item = XianhuoItem()
            item["model"] = i.xpath('div[@class="item-head"]/div[@class="item-head-center"]/div/div/div[contains(@class,"ellipsis")]/@title').extract_first()
            item["brand"] = i.xpath('div[@class="item-head"]/div[@class="item-head-center"]/div/div[2]/div/text()').extract()[-1]
            item["price"] = json.dumps(i.xpath('div[@class="item-table-center"]/table[@class="table"]/tbody/tr/td[@class="children"]//span/text()').re("￥(.*)"))
            item["levels"] = json.dumps(i.xpath('div[@class="item-table-center"]/table[@class="table"]/tbody/tr/td[@class="children"]//td/text()').re("(.*?)\\+"))
            item["shop"] = "拍明芯城"
            item["status"] = "1"
            yield item
        next = response.xpath('body/div[contains(@class,"container-fluid")]/div[contains(@class,"apps")]/div[contains(@class,"main-content")]/div[contains(@class,"tab-content")]//div[@align="right"]/a/@href').extract()[-1]
        url = response.urljoin(next)
        yield scrapy.Request(url=url, callback=self.parse,dont_filter=True)