# -*- coding: utf-8 -*-

import pymongo

from scrapy.exceptions import DropItem
from scrapy.conf import settings
from scrapy import log

class DoubanmoviePipeline(object):
    #Connect to the MongoDB database
    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        print("item->", item)
        #Remove invalid data
        valid = True
        for data in item:
          if not data:
            valid = False
            raise DropItem("Missing %s of blogpost from %s" %(data, item['url']))
        if valid:
            new_moive=[{
                "name":item['name'],
                "year":item['year'],
                "score":item['score'],
                "director":item['director'],
                "classification":item['classification'],
                "actor":item['actor']
            }]
            self.collection.insert(new_moive)
            log.msg("Item wrote to MongoDB database %s/%s" %
                    (settings['MONGODB_DB'], settings['MONGODB_COLLECTION']),
            level=log.DEBUG, spider=spider)
        return item