import scrapy
from scrapy.crawler import CrawlerProcess
from crawljobdata.crawljobdata.spiders import careerbuilder, careerlink, a123job, jobsgo, viectotnhat ,vieclam1001, timviec365_vn, timviecnhanh_com, vieclam24h_vn, vietnamwork


process = CrawlerProcess()
process.crawl(vieclam1001.vieclam1001)
process.crawl(careerbuilder.CareerBuilder)
process.crawl(timviec365_vn.TimViec365Spider)
process.crawl(vieclam24h_vn.ViecLam24hSpider)
process.crawl(viectotnhat.ViectotnhatSpider)
process.crawl(jobsgo.JobsgoSpider)
# process.crawl(a123job.A123jobSpider)
# process.crawl(careerlink.CareerLink)
# process.crawl(timviecnhanh_com.TimViecNhanhSpider)
# process.crawl(vietnamwork.vietnamworks)
process.start() # the script will block here until all crawling jobs are finished