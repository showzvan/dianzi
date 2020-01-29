# -*- coding: utf-8 -*-
import scrapy


class WeiyangSpider(scrapy.Spider):
    name = 'weiyang'
    allowed_domains = ['https://www.oneyac.com/']
    start_urls = ['https://soic.oneyac.com/search']
    # callback: jQuery1124015372640916829927_1579397317429
    # paramsDTO: {"page": "0", "categoryId": "", "supplierId": "1", "keyword": "", "brand_id_filters[]": ["1062"],
    #             "token": "on@hol11LvcSUKNadAU!xm@GbUl38b7gP2jOTd7O1wynoKkqdrDlS7eg7BRJuIz7pUjeyac$der"}
    param = {
        "callback": "jQuery1124015372640916829927_1579397317429",
        "paramsDTO": {
            "page": "0",
            "categoryId": "",
            "supplierId": "1",
            "keyword": "",
            "brand_id_filters[]": ["1062"],
            "token": "on@hol11LvcSUKNadAU!xm@GbUl38b7gP2jOTd7O1wynoKkqdrDlS7eg7BRJuIz7pUjeyac$der"
        }
    }

    def parse(self, response):
        print(response.text)
        # list_table = response.css("#list_tbody_list")
        # print(len(list_table))