# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider
from scrapy.selector import Selector

from hackernews.items import HackernewsItem


class BasicSpider(scrapy.Spider):
    name = "basic"
    allowed_domains = ["news.ycombinator.com"]
    start_urls = ['http://news.ycombinator.com/']

    def parse(self, response):
        titles = Selector(response).xpath('//tr[@class="athing"]/td[3]')
        
        for title in titles:
            item = HackernewsItem()
            item['title'] = title.xpath("a[@href]/text()").extract()
            item['url'] = title.xpath("a/@href").extract()
            yield item
