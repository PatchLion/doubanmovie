# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class DoubanmoiveItem(Item):
    name = Field() #电影名
    year = Field() #上映年份
    score = Field() #豆瓣分数
    director = Field() #导演
    classification = Field() #分类
    actor = Field() #演员
    imageurl = Field() #图片url
