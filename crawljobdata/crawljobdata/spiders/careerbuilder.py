import scrapy
# from ..items import CrawldataItem
import re
from pymongo import MongoClient

myclient = MongoClient("mongodb://localhost:27017/")
mydb = myclient["crawljob"]
mycol = mydb["careerbuilder"]
with open('link.txt', mode='r') as f:
    links = f.read().split('\n')

class CareerBuilder(scrapy.Spider):
    name = 'careerbuilder'
    allow_domains = ['careerbuilder.vn']
    start_urls = [
            'https://careerbuilder.vn/viec-lam/tat-ca-viec-lam-vi.html'
        ]
    # link = 0
    def parse(self, response):
        urls = response.xpath('//a[contains(@class, "job_link")]/@href').getall()
        for url in urls:
            if url not in links:
                url = response.urljoin(url)
                yield scrapy.Request(url=url, callback=self.parse_details)
        next_page_url = response.xpath('//li[contains(@class, "next-page")]/a/@href').get()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            # self.link = next_page_url
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_details(self, response):
        
        # data = CrawldataItem()
        data = {}
        data['url'] = response.url
        data['title'] = response.xpath('//div[contains(@class, "job-desc")]/h1/text()').get()

        data['factory'] = response.xpath('//a[contains(@class, "employer job-company-name")]/text()').get()

        data['city'] = response.xpath('//div[contains(@class, "map")]/p/a/text()').get()

        m = response.xpath('//strong[contains(text(),"Ngày cập nhật")]')
        n = m.xpath('string(following-sibling::p)').get()
        if n is not None:
            data['Ngày cập nhật'] = n.strip()
        else: data['Ngày cập nhật'] = ''

        careers = response.xpath('//div[contains(@class, "detail-box has-background")]/ul/li/p/a/text()').getall()
        data['Ngành nghề'] = [career.strip() for career in careers]

        m = response.xpath('//strong[contains(text(),"Hình thức")]')
        n = m.xpath('string(following-sibling::p)').get()
        if n is not None:
            data['Hình thức'] = n.strip()
        else: data['Hình thức'] = ''

        m = response.xpath('//strong[contains(text(),"Lương")]')
        n = m.xpath('string(following-sibling::p)').get()
        if n is not None:
            data['Lương'] = n.strip()
        else: data['Lương'] = ''

        m = response.xpath('//strong[contains(text(),"Kinh nghiệm")]')
        n = m.xpath('string(following-sibling::p)').get()
        if n is not None:
            data['Kinh nghiệm'] = n.strip()
        else: data['Kinh nghiệm'] = ''

        m = response.xpath('//strong[contains(text(),"Cấp bậc")]')
        n = m.xpath('string(following-sibling::p)').get()
        if n is not None:
            data['Cấp bậc'] = n.strip()
        else: data['Cấp bậc'] = ''

        m = response.xpath('//strong[contains(text(),"Hết hạn nộp")]')
        n = m.xpath('string(following-sibling::p)').get()
        if n is not None:
            data['Hết hạn nộp'] = n.strip()
        else: data['Hết hạn nộp'] = ''

        
        m = response.xpath('//div[contains(@class, "detail-row")]').getall()
        n = ['Phúc lợi', 'Mô tả công việc', 'Yêu cầu công việc', 'Thông tin khác']
        for i in range(len(n)):
            data[n[i]] = re.sub('<.*?>', '', m[i].strip()).strip()
        m = response.xpath('//div[contains(@class, "job-tags")]/ul/li/a/text()').getall()
        if m is not None:
            m = [i.strip() for i in m]
            data['jobtags/skill'] = m
        else: data['jobtags/skill'] = ''
        mycol.insert_one(data)
        yield data