import scrapy
# from ..items import CrawldataItem
import re
from pymongo import MongoClient

myclient = MongoClient("mongodb://localhost:27017/")
mydb = myclient["crawljob"]
mycol = mydb["viectotnhat"]

class viectotnhat(scrapy.Spider):
    name = 'viectotnhat'
    allow_domains = ['viectotnhat.com']
    start_urls = [
            'https://viectotnhat.com/viec-lam/tim-kiem?tu_khoa=&nganh_nghe=0&tinh_thanh=0'
        ]
    # link = 0
    def parse(self, response):
        urls = response.xpath('//h3[contains(@class, "job-name margin0")]/a/@href').getall()
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_details)
        next_page_url = response.xpath('//a[contains(@aria-label, "Next")]/@href').get()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            # self.link = next_page_url
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_details(self, response):
        
        # data = CrawldataItem()
        data = {}
        data['url'] = response.url
        data['title'] = response.xpath('//h1/text()').get()

        data['factory'] = response.xpath('//h2[contains(@class,"fontSize16")]/text()').get()

        data['deadline'] = response.xpath('//span[contains(@class,"color-orange2")]/text()').get().strip()

        m = response.xpath('//ul[contains(@style,"padding-left: 0px;")]/li/text()').getall()
        m = [i.strip() for i in m]
        n = response.xpath('//span[contains(@class, "font600")]/text()').getall()
        n = [i.strip() for i in n]
        n = [i[:-1] for i in n]
        if 'Số lượng cần tuyển' in n: n.remove('Số lượng cần tuyển')
        if 'Địa điểm làm việc'  in n: n.remove('Địa điểm làm việc')
        if 'Ngành nghề' in n: n.remove('Ngành nghề')
        while(1):
            if '' in m: m.remove('')
            elif ',' in m: m.remove(',')
            else: break
        k = list()
        for i in range(len(m)):
            if m[i] in k: break
            else: k.append(m[i])

        for i in range(len(m)):
            data[n[i]] = m[i]

        data['Số lượng cần tuyển'] = response.xpath('//ul[contains(@style,"padding-left: 0px;")]/li[4]/span[2]/text()').getall()[1]
        m = response.xpath('//a[contains(@class, "text-primary")]/text()').getall()
        data['career'] = m[:2]
        data['city'] = m[2]

        # m = response.xpath('//div[contains(@class, "fontSize22")]/text()').getall()
        mota = response.xpath('//div[contains(@class, "mo-ta-cv")]').get()
        data['Mô tả công việc'] = re.sub('<.*?>', ' ', mota.strip()).strip()
        
        yeucau = response.xpath('//div[contains(@class, "yeu-cau")]').get()
        data['Yêu cầu công việc'] = re.sub('<.*?>', ' ', yeucau.strip()).strip()

        quyenloi = response.xpath('//div[contains(@class, "quyen-loi")]').get()
        data['Quyền lợi'] = re.sub('<.*?>', ' ', quyenloi.strip()).strip()
        
        m =  response.xpath('//div[contains(@class, "ho-so")]/ul/li/span/text()').getall()
        m = [i[:-1] for i in m]
        n = response.xpath('//div[contains(@class, "ho-so")]/ul/li/text()').getall()
        n = [i.strip() for i in n]
        for i in range(len(m)):
            data[m[i]] = n[i]
        mycol.insert_one(data)
        yield data