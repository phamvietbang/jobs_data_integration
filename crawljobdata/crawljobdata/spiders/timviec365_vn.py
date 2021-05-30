import scrapy
from scrapy.loader import ItemLoader
from ..items import JobNewsItem
from datetime import datetime
from pymongo import MongoClient

myclient = MongoClient("mongodb://localhost:27017/")
mydb = myclient["crawljob"]
mycol = mydb["job_news"]

class TimViec365Spider(scrapy.Spider):
    name = "timviec365"
    source = "timviec365.vn"
    # allowed_domains = [""]
    start_urls = ['https://timviec365.vn/tin-tuyen-dung-viec-lam.html?page=1']

    def parse(self, response):
        detail_pages = response.css('a.title_cate::attr(href)').getall()
        for i in range(len(detail_pages)):
            detail_page = response.urljoin(detail_pages[i])
            yield scrapy.Request(detail_page, callback=self.parse_detail, dont_filter=False) # dont_filter=False means scrapy will not get duplicate links
                # yield scrapy.Request(author_page, callback=self.parse_author, \
                #     meta={'quote_item': quote_item})
            # else:
            #     print('none')
            # yield response.follow(author_page, self.parse_author, meta={'quote_item': quote_item})
        
        next_page = response.css('a.next::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
        
        '''
        # use when cannot get href from next button
        n_news = int(response.css('.text-speci.mx-1::text').get())
        N_NEWS_PER_PAGE = 20
        n_pages = n_news//N_NEWS_PER_PAGE
        if n_pages*N_NEWS_PER_PAGE < n_news:
            n_pages += 1
        base_urls = 'https://vieclam24h.vn/tim-kiem-viec-lam-nhanh?q=&province_ids=&field_ids&action=search&page='
        for i in range(2, n_pages+1):
            yield scrapy.Request(base_urls + str(i), callback=self.parse)
        '''
    def parse_detail(self, response):
        # quote_item = response.meta['quote_item']
        item = JobNewsItem()
        loader = ItemLoader(item=item, response=response)
        loader.add_value('source', self.source)
        now = datetime.now()
        loader.add_value('crawled_time', [now.strftime("%d/%m/%Y %H:%M:%S")])
        loader.add_value('news_link', [response.url])
        loader.add_css('title', '.right_tit>h1::text')
        loader.add_css('salary', '.lv_luong>span::text')
        number_available = response.css('b:contains("Số lượng cần tuyển:")+span::text').get()
        number_available = number_available.replace('ứng viên', '').strip()
        loader.add_value('number_available', number_available)
        description = response.css('div:contains("Mô tả công việc")::text').getall()
        description = [d.replace('\n', '').strip() for d in description]
        description = [d[1:].strip() for d in description if not d == '']
        loader.add_value('description', description)
        benefits = response.css(".box_quyenloi")[0].css("::text").getall()
        benefits.remove('Quyền lợi được hưởng')
        benefits = [b[1:] for b in benefits if not b.startswith('\n')]
        benefits = [b.strip() for b in benefits]
        loader.add_value('benefits', benefits)
        loader.add_css('working_location', '.dd_tuyen>a::text')
        loader.add_css('position', 'b:contains("Chức vụ:")+span::text')
        loader.add_css('types', 'div:contains("Ngành nghề:")>a::text')
        loader.add_css('experience', 'b:contains("Kinh nghiệm:")+span::text')
        degree = response.css('b:contains("Yêu cầu bằng cấp:")+span::text').get()
        loader.add_value('degree', degree.replace('trở lên', '').strip())
        loader.add_css('gender', 'b:contains("Yêu cầu giới tính:")+span::text')
        updated_date = response.css('p:contains("Ngày cập nhật:")::text').get()
        updated_date =  updated_date.replace('Ngày cập nhật:', '')
        updated_date =  updated_date.replace('\n', '').strip()
        loader.add_value('updated_date', updated_date)
        deadline = response.css('p:contains("Hạn nộp hồ sơ:")>span::text').get()
        deadline = deadline.replace('\n', '').strip()
        loader.add_value('deadline', deadline)
        requirements = response.css('div.box_yeucau:contains("Yêu cầu công việc")::text').getall()
        requirements = [d.replace('\n', '').strip() for d in requirements]
        requirements = [d[1:].strip() for d in requirements if not d == '']
        loader.add_value('requirements', requirements)
        loader.add_css('company_name', '.right_tit>p>a::text')
        company_link = response.css('.right_tit>p>a::attr(href)').get()
        company_link = response.urljoin(company_link)
        loader.add_value('company_link', company_link)
        loader.add_css('company_address', 'p.dd_dc>span::text')
        mycol.insert_one(loader.load_item())
        yield loader.load_item()

        