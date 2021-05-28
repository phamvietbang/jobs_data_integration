import scrapy
from scrapy.loader import ItemLoader
from crawljobdata.items import JobNewsItem
from datetime import datetime
from pymongo import MongoClient
myclient = MongoClient("mongodb://localhost:27017/")
mydb = myclient["crawljob"]
mycol = mydb["job_news"]
class TimViecNhanhSpider(scrapy.Spider):
    name = "timviecnhanh"
    source = "timviecnhanh.com"
    # allowed_domains = [""]
    start_urls = ['https://timviecnhanh.com/vieclam/timkiem?action=search&q=&page=1']

    def parse(self, response):
        detail_pages = response.css('a.title-job::attr(href)').getall()
        for i in range(len(detail_pages)):
            detail_page = response.urljoin(detail_pages[i])
            yield scrapy.Request(detail_page, callback=self.parse_detail, dont_filter=False) # dont_filter=False means scrapy will not get duplicate links
                # yield scrapy.Request(author_page, callback=self.parse_author, \
                #     meta={'quote_item': quote_item})
            # else:
            #     print('none')
            # yield response.follow(author_page, self.parse_author, meta={'quote_item': quote_item})
        '''
        next_page = response.css('a.next::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
        '''
        
        # use when cannot get href from next button
        n_news = int(response.css('span.count::text').get()[1:-1])
        N_NEWS_PER_PAGE = 20
        n_pages = n_news//N_NEWS_PER_PAGE
        if n_pages*N_NEWS_PER_PAGE < n_news:
            n_pages += 1
        base_urls = 'https://timviecnhanh.com/vieclam/timkiem?action=search&q=&page='
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
        loader.add_css('title', 'span.title::text')
        loader.add_css('salary', 'li:contains("Mức lương:")::text')
        loader.add_css('number_available', 'li:contains("Số lượng tuyển dụng:")::text')
        # description = response.xpath('//b[contains(text(), "Mô tả")]/../following-sibling::td')
        # description = description.css('p::text').getall()
        loader.add_css('description', 'td:contains("Mô tả")+td>p::text')
        # benefits = response.xpath('//b[contains(text(), "Quyền lợi")]/../following-sibling::td')
        # benefits = benefits.css('p::text').getall()
        loader.add_css('benefits', 'td:contains("Quyền lợi")+td>p::text')
        loader.add_css('working_location', 'b:contains("Tỉnh/Thành phố")+a::text')
        loader.add_value('position', '')
        loader.add_css('types', 'li:contains("Ngành nghề")>a::text')
        loader.add_css('experience', 'li:contains("Kinh nghiệm:")::text')
        loader.add_css('degree', 'li:contains("Trình độ")::text')
        loader.add_css('gender', 'li:contains("Giới tính")::text')
        updated_date = response.css('div:contains("Cập nhật:")::text').get()
        updated_date =  updated_date.replace('Cập nhật:', '').strip()
        updated_date = datetime.strptime(updated_date, '%d-%m-%Y').strftime('%d/%m/%Y')
        loader.add_value('updated_date', updated_date)
        deadline = response.css('td:contains("Hạn nộp")+td ::text').get()
        deadline = datetime.strptime(deadline, '%d-%m-%Y').strftime('%d/%m/%Y')
        loader.add_value('deadline', deadline)
        loader.add_css('requirements', 'td:contains("Yêu cầu")+td>p::text')
        loader.add_css('company_name', 'a.company-work::text')
        company_link = response.css('a.company-work::attr(href)').get()
        company_link = response.urljoin(company_link)
        loader.add_value('company_link', company_link)
        company_address = response.css('h3+span:contains("Địa chỉ")::text').get()
        company_address = company_address.replace('Địa chỉ:', '').strip()
        loader.add_value('company_address', company_address)
        mycol.insert_one(loader.load_item())
        yield loader.load_item()

        