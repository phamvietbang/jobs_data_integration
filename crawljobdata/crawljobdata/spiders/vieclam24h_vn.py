import scrapy
from scrapy.loader import ItemLoader
from ..items import JobNewsItem
from datetime import datetime
from pymongo import MongoClient
myclient = MongoClient("mongodb://localhost:27017/")
mydb = myclient["crawljob"]
mycol = mydb["job_news"]

class ViecLam24hSpider(scrapy.Spider):
    name = "vieclam24h"
    source = "vieclam24h.vn"
    # allowed_domains = [""]
    start_urls = ['https://vieclam24h.vn/tim-kiem-viec-lam-nhanh?q=&province_ids=&field_ids&action=search&page=1']

    def parse(self, response):
        news = response.css('.job-box')
        for news_i in news:
            urls = news_i.css('a')
            detail_page = urls[0].css('::attr(href)').get()

            if detail_page is not None:
                detail_page = response.urljoin(detail_page)
                yield scrapy.Request(detail_page, callback=self.parse_detail, dont_filter=False) # dont_filter=False means scrapy will not get duplicate links
                # yield scrapy.Request(author_page, callback=self.parse_author, \
                #     meta={'quote_item': quote_item})
            # else:
            #     print('none')
            # yield response.follow(author_page, self.parse_author, meta={'quote_item': quote_item})
        
        # next_page = response.css('li.next a::attr(href)').get()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)
        
        n_news = int(response.css('.text-speci.mx-1::text').get())
        N_NEWS_PER_PAGE = 20
        n_pages = n_news//N_NEWS_PER_PAGE
        if n_pages*N_NEWS_PER_PAGE < n_news:
            n_pages += 1
        base_urls = 'https://vieclam24h.vn/tim-kiem-viec-lam-nhanh?q=&province_ids=&field_ids&action=search&page='
        for i in range(2, n_pages+1):
            yield scrapy.Request(base_urls + str(i), callback=self.parse)

    def parse_detail(self, response):
        # quote_item = response.meta['quote_item']
        item = JobNewsItem()
        loader = ItemLoader(item=item, response=response)
        loader.add_value('source', self.source)
        now = datetime.now()
        loader.add_value('crawled_time', [now.strftime("%d/%m/%Y %H:%M:%S")])
        loader.add_value('news_link', [response.url])
        loader.add_css('title', '.title-job::text')
        loader.add_css('salary', '.job_value::text')
        loader.add_css('number_available', 'span:contains("S??? l?????ng c???n tuy???n:")+span::text')
        loader.add_css('description', 'div:contains("M?? t??? c??ng vi???c")+div::text')
        loader.add_css('benefits', 'div:contains("Quy???n l???i ???????c h?????ng")+p::text')
        loader.add_css('working_location', 'span:contains("?????a ??i???m l??m vi???c:")+a::text')
        loader.add_css('position', 'span:contains("Ch???c v???:")>span::text')
        types = response.css('div:contains("Ng??nh ngh???:")>a::text').getall()
        types = types[:len(types)//2]
        loader.add_value('types', types)
        loader.add_css('experience', 'span:contains("Kinh nghi???m:")+span::text')
        loader.add_css('degree', 'span:contains("Y??u c???u b???ng c???p:")+span::text')
        loader.add_css('gender', 'span:contains("Y??u c???u gi???i t??nh:")+span::text')
        updated_date = response.css('span:contains("Ng??y l??m m???i:")::text').get()
        updated_date =  updated_date.replace('Ng??y l??m m???i: ', '')
        loader.add_value('updated_date', updated_date)
        loader.add_css('deadline', 'span:contains("H???n n???p h??? s??:")+span::text')
        loader.add_css('requirements', 'div:contains("Y??u c???u kh??c")+p::text')
        #degree, gender, updated_date, deadline

        loader.add_css('company_name', '.title-company>a::text')
        company_link = response.css('.title-company>a::attr(href)').get()
        company_link = response.urljoin(company_link)
        loader.add_value('company_link', company_link)
        loader.add_css('company_address', 'span:contains("?????a ch???:")+span::text')
        mycol.insert_one(loader.load_item())    
        yield loader.load_item()

        