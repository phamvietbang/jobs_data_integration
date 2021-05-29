# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    job_desc = scrapy.Field()
    job_req = scrapy.Field()
    job_ben = scrapy.Field()
    job_pos = scrapy.Field()
    salary = scrapy.Field()
    age = scrapy.Field()
    gender = scrapy.Field()
    com_name = scrapy.Field()
    com_add = scrapy.Field()
    job_nums_avai = scrapy.Field()
    job_exp = scrapy.Field()
    location = scrapy.Field()
    certificate = scrapy.Field()
    deadline = scrapy.Field()
    info = scrapy.Field()
    url = scrapy.Field()
    time_collect = scrapy.Field()
    types = scrapy.Field()