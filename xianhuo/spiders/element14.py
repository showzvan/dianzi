# -*- coding: utf-8 -*-
import scrapy


class Element14Spider(scrapy.Spider):
    name = 'element14'
    allowed_domains = ['https://cn.element14.com']
    start_urls = ['https://cn.element14.com/search/prl/results?brand=te-connectivity']

    def parse(self, response):
        # altRows = response.xpath('div[@class="innerWraper"]/table[@class="sProdList"]/tbody/tr[@class="altRow"]')
        altRows = response.css('#sProdList tbody tr')
        print(len(altRows))
        a = 1
        # for altRow in altRows:
        #     # a += 1
        #     # print(a)
        #     model = altRow.xpath('td[contains(@class,"productImage")]/input[@class="hVal"]/@value').extract_first()
        #     print(model)

