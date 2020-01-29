# -*- coding: utf-8 -*-
import scrapy
import json
from xianhuo.items import XianhuoItem

"""
2020.1.8 爬取至：https://www.mouser.cn/Search/Refine?N=4292733690&No=121900
下次开始：https://www.mouser.cn/Search/Refine?N=4292733690&No=121900
"""

class MouserSpider(scrapy.Spider):
    name = 'mouser'
    allowed_domains = ['https://www.mouser.cn']
    start_urls = ['https://www.mouser.cn/Search/Refine?N=4292733690&No=121925']

    def parse(self, response):
        resultsTables = response.xpath('//table[@id="SearchResultsGrid_grid"]/tbody/tr')
        for i in resultsTables:
            item = XianhuoItem()
            item["model"] = i.xpath('td[contains(@class,"part-column")]/div[@class="mfr-part-num "]/a[@id="lnkMfrPartNumber"]/text()').extract_first()
            item["brand"] = i.xpath('td[contains(@class,"mfr-column")]/a[@id="lnkSupplierPage"]/text()').extract_first()
            item["shop"] = "mouser"
            item["price"] = json.dumps(i.xpath('td[contains(@class,"text-center")]/table[@class="search-pricing-table"]//span[@id="lblPrice"]/text()').re('¥(.*)'))
            item["levels"] = json.dumps(i.xpath('td[contains(@class,"text-center")]/table[@class="search-pricing-table"]//a[@id="lnkQuantity"]/text()').re('(.*?):'))
            item["status"] = "1"
            yield item

        next = response.css('#lnkPager_lnkNext::attr(href)').extract_first()
        # print(next)
        url = response.urljoin(next)
        # print(url)
        yield scrapy.Request(url=url, callback=self.parse,dont_filter=True)
