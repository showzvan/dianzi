# -*- coding: utf-8 -*-
import scrapy


class LiexinSpider(scrapy.Spider):
    name = 'liexin'
    allowed_domains = ['https://www.ichunt.com/']
    start_urls = ['http://https://www.ichunt.com//']

    def parse(self, response):
        pass
