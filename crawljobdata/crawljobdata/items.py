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