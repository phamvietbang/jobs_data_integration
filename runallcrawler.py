import scrapy
from scrapy.crawler import CrawlerProcess
from crawljobdata.crawljobdata.spiders import 1001vieclam, careerbuilder, careerlink, timviec365_vn, timviecnhanh_com,vieclam24h_vn, viectotnhat, vietnamwork


process = CrawlerProcess()
process.crawl(1001vieclam.vieclam1001)
process.crawl(careerbuilder.CareerBuilder)
process.crawl(careerlink.CareerLink)
process.crawl(timviec365_vn.TimViec365Spider)
process.crawl(timviecnhanh_com.TimViecNhanhSpider)
process.crawl(vieclam24h_vn.ViecLam24hSpider)
process.crawl(viectotnhat.viectotnhat)
process.crawl(vietnamwork.vietnamworks)
process.start() # the script will block here until all crawling jobs are finished