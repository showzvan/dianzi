# -*- coding: utf-8 -*-
import scrapy
import json
from xianhuo.items import XianhuoItem


class LichuangSpider(scrapy.Spider):
    name = 'lichuang'
    allowed_domains = ['https://www.szlcsc.com/']
    start_urls = ['https://list.szlcsc.com/brand_page/109.html']

    def parse(self, response):
        insides = response.css('.inside')
        for i in insides:
            item = XianhuoItem()
            # 料号
            item["model"] = i.xpath('tbody/tr/td[@class="two"]/div[@class="two-01"]/ul[@class="l02-yb"]/li/span/@title').extract_first()
            # 品牌
            item["brand"] = i.xpath('tbody/tr/td[@class="two"]/div[@class="two-01"]/ul[@class="l02-yb"]/li[@class="band"]/a/text()').extract_first().strip()
            # 价格
            item["price"] = json.dumps(i.xpath('tbody/tr/td[@class="three"]/ul[@class="three-nr"]/li/span[contains(@class,"ccd")]/@data-productprice').extract())
            # 价格阶梯
            item["levels"] = json.dumps(i.xpath('tbody/tr/td[@class="three"]/ul[@class="three-nr"]/li/p[@class="ppbbz-p"]/text()').re('(\d+)+'))
            # 商城
            item["shop"] = "立创商城"
            # 状态
            item["status"] = "1"
            yield item
        # 当前页码
        next = response.css('.page-link-page-util .page-left li a.active::text').extract_first()
        # 最后一页的页码
        last_page = response.css('.page-link-page-util .page-right input::attr(value)').extract_first()
        if int(next) == int(last_page):
            print ("it is end")
            return
        data = {
            "pageNumber": str(int(next) + 1)
        }
        yield scrapy.FormRequest(method='POST', url=self.start_urls[0], formdata=data, callback=self.parse, dont_filter=True)
