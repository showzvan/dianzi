# -*- coding: utf-8 -*-
import scrapy
import requests
import json
from time import time


class WeiyangSpider(scrapy.Spider):
    name = 'weiyang'
    allowed_domains = ['https://www.oneyac.com/']
    start_urls = ['https://soic.oneyac.com/search']

    data = {
        "callback": "jQuery112402324948714089965_" + str(round(time())),
        "paramsDTO": {
                "page": 1,
                "categoryId": "",
                "supplierId": "1",
                "keyword": "",
                "brand_id_filters[]": ["1062"],
                # "token": "on@hol11fw3q78thl1n!xm@a83ju4gaae1u896ja1wynoxev5kufvki2w8oue20q9zoeyac$der"
        },
        "_": str(round(time()))
    }

    def start_requests(self):
        print(self.data)
        response = scrapy.FormRequest(method='POST', url=self.start_urls[0], formdata=self.data, callback=self.parse, dont_filter=True)
        # print(response.text)
        yield response


    def parse(self, response):
        print(response.text)
        # list_table = response.css("#list_tbody_list")
        # print(len(list_table))
        # pass