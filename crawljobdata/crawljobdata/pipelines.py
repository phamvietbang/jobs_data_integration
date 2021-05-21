# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

class CrawljobdataPipeline:
    def __init__(self):
        self.conn = MongoClient('localhost',27017)
        db = self.conn['data']
        self.collection = db['job3']
    def process_item(self, item, spider):
        self.collection.insert_one(item)                #save to databases
        return item
