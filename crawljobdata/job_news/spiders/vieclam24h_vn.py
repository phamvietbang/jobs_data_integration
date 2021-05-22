import scrapy
from scrapy.loader import ItemLoader
from job_news.items import JobNewsItem
from datetime import datetime

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
        loader.add_css('number_available', 'span:contains("Số lượng cần tuyển:")+span::text')
        loader.add_css('description', 'div:contains("Mô tả công việc")+div::text')
        loader.add_css('benefits', 'div:contains("Quyền lợi được hưởng")+p::text')
        loader.add_css('working_location', 'span:contains("Địa điểm làm việc:")+a::text')
        loader.add_css('position', 'span:contains("Chức vụ:")>span::text')
        types = response.css('div:contains("Ngành nghề:")>a::text').getall()
        types = types[:len(types)//2]
        loader.add_value('types', types)
        loader.add_css('experience', 'span:contains("Kinh nghiệm:")+span::text')
        loader.add_css('degree', 'span:contains("Yêu cầu bằng cấp:")+span::text')
        loader.add_css('gender', 'span:contains("Yêu cầu giới tính:")+span::text')
        updated_date = response.css('span:contains("Ngày làm mới:")::text').get()
        updated_date =  updated_date.replace('Ngày làm mới: ', '')
        loader.add_value('updated_date', updated_date)
        loader.add_css('deadline', 'span:contains("Hạn nộp hồ sơ:")+span::text')
        loader.add_css('requirements', 'div:contains("Yêu cầu khác")+p::text')
        #degree, gender, updated_date, deadline

        loader.add_css('company_name', '.title-company>a::text')
        company_link = response.css('.title-company>a::attr(href)').get()
        company_link = response.urljoin(company_link)
        loader.add_value('company_link', company_link)
        loader.add_css('company_address', 'span:contains("Địa chỉ:")+span::text')
               
        yield loader.load_item()

        