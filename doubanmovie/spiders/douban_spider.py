# -*- coding: utf-8 -*-

from scrapy.selector import Selector
from scrapy.contrib.spiders import Spider, Rule
#from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from doubanmovie.items import DoubanmoiveItem
from scrapy.http import HtmlResponse
from scrapy.http import Request


def replaceGBKChar(string):
    return string.replace(u"\xa0", u"").replace(u"\xee", u"").replace(u"\xf6", u"")

class DoubanspiderSpider(Spider):
    name = "doubanspider"
    allowed_domains = ["movie.douban.com"]
    start_urls = ['http://movie.douban.com/top250']

    '''rules = [
        Rule(SgmlLinkExtractor(allow=r'http://movie.douban.com/top250\?start=\d+.*')),
        Rule(SgmlLinkExtractor(allow=r'http://movie.douban.com/subject/\d+'), callback="parse_item")
    ]
    '''

    def parse(self, response):
        sel=Selector(text=response.body.decode('utf-8', 'ignore'))
        movie_items = sel.xpath("//div[@class='item']")
        for mi in movie_items:
            url = mi.xpath("div[@class='pic']/a/@href").extract()[0]
            print("url->", url)
            yield Request(url, callback=self.parse_item)

    def parse_item(self, response):
        item = DoubanmoiveItem()
        sel = Selector(response)
        item["name"] = sel.xpath("//div[@id='content']/h1/span[1]/text()").extract()[0]
        item["year"] = sel.xpath("//div[@id='content']/h1/span[2]/text()").extract()[0].replace("(", "").replace(")", "")
        item["score"] = sel.xpath("//div[@class='rating_self clearfix']/strong/text()").extract()[0]
        item["director"] = sel.xpath("//div[@id='info']/span[1]/span[2]/a/text()").extract()[0]
        item["classification"] = " ".join(sel.xpath('//span[@property="v:genre"]/text()').extract())
        item["actor"] = " ".join(sel.xpath("//div[@id='info']/span[@class='actor']/span[@class='attrs']/*/text()").extract())
        item["imageurl"] = sel.xpath("//div[@id='mainpic']/a/img/@src").extract()[0]
        return item