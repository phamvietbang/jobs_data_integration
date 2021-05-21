import scrapy
from scrapy.crawler import CrawlerProcess
from spiders import careerbuilder
from scrapy.utils.project import get_project_settings
process = CrawlerProcess(get_project_settings())
process.crawl(careerbuilder.CareerBuilder)
process.start()