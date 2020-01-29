# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XianhuoItem(scrapy.Item):
    # 抓取内容：1.料号 2.价格 3.价格梯度 4.品牌 5.商城名
    model = scrapy.Field()
    price = scrapy.Field()
    levels = scrapy.Field()
    brand = scrapy.Field()
    shop = scrapy.Field()
    status = scrapy.Field()