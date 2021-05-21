import scrapy
import re


class vieclam1001(scrapy.Spider):
    name = '1001vieclam'
    allow_domains = ['1001vieclam.vn']
    start_urls = [
        'https://1001vieclam.com/search-results-jobs/?action=search&listing_type%5Bequal%5D=Job&'
    ]

    def parse(self, response):
        urls = response.xpath('//h3/a/@href').getall()
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_details)
        next_page_url = response.xpath('//span[contains(@class, "nextBtn")]/a/@href').get()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            print(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_details(self, response):

        data = {}
        data['url'] = response.url
        data['title'] = response.xpath('//h1/text()').get()
        data['factory'] = response.xpath('//span[contains(@class, "company-name")]/text()').get()

        m = response.xpath('//h3[contains(text(),"Nơi làm việc:")]')
        n = m.xpath('string(following-sibling::div[1])').get()
        if n is not None:
            data['Nơi làm việc'] = n.strip()

        m = response.xpath('//h3[contains(text(),"Ngành:")]')
        n = m.xpath('string(following-sibling::div[1])').get()
        if n is not None:
            data['Ngành'] = n.strip()
        
        m = response.xpath('//h3[contains(text(),"Lương:")]')
        n = m.xpath('string(following-sibling::div[1])').get()
        if n is not None:
            data['Lương'] = n.strip()

        m = response.xpath('//h3[contains(text(),"Mức thưởng:")]')
        n = m.xpath('string(following-sibling::div[1])').get()
        if n is not None:
            data['Mức thưởng'] = n.strip()

        m = response.xpath('//h3[contains(text(),"Hình thức làm việc:")]')
        n = m.xpath('string(following-sibling::div[1])').get()
        if n is not None:
            data['Hình thức làm việc'] = n.strip()

        m = response.xpath('//h3[contains(text(),"ID công việc:")]')
        n = m.xpath('string(following-sibling::div[1])').get()
        if n is not None:
            data['ID công việc'] = n.strip()

        m = response.xpath('//h3[contains(text(),"Ngày hết hạn:")]')
        n = m.xpath('string(following-sibling::div[1])').get()
        if n is not None:
            data['Ngày hết hạn'] = n.strip()

        m = response.xpath('//h3[contains(text(),"Mô tả công việc:")]')
        data['Mô tả công việc'] = m.xpath('string(following-sibling::div[1])').get()

        m = response.xpath('//h3[contains(text(),"Yêu cầu công việc:")]')
        data['Yêu cầu công việc'] = m.xpath('string(following-sibling::div[1])').get()

        m = response.xpath('//h3[contains(text(),"Quyền lợi:")]')
        data['Quyền lợi'] = m.xpath('string(following-sibling::div[1])').get()

        yield  data