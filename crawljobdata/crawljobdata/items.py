# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


import scrapy
from scrapy.loader.processors import TakeFirst

class JobNewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    source = scrapy.Field(output_processor=TakeFirst())
    crawled_time = scrapy.Field(output_processor=TakeFirst())
    news_link = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(output_processor=TakeFirst())
    salary = scrapy.Field(output_processor=TakeFirst())
    number_available = scrapy.Field(output_processor=TakeFirst())
    description = scrapy.Field()
    benefits = scrapy.Field()
    working_location = scrapy.Field(output_processor=TakeFirst())
    position = scrapy.Field(output_processor=TakeFirst())
    types = scrapy.Field()
    experience = scrapy.Field(output_processor=TakeFirst())
    degree = scrapy.Field(output_processor=TakeFirst())
    gender = scrapy.Field(output_processor=TakeFirst())
    updated_date = scrapy.Field(output_processor=TakeFirst())
    deadline = scrapy.Field(output_processor=TakeFirst())
    requirements = scrapy.Field()

    company_name = scrapy.Field(output_processor=TakeFirst())
    company_address = scrapy.Field(output_processor=TakeFirst())    
    company_link = scrapy.Field(output_processor=TakeFirst())

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