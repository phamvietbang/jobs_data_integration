import scrapy
import re
from pymongo import MongoClient

myclient = MongoClient("mongodb://localhost:27017/")
mydb = myclient["crawljob"]
mycol = mydb["careerlink"]
with open('link.txt', mode='r') as f:
    links = f.read().split('\n')
class CareerLink(scrapy.Spider):
    name = 'careerlink'
    allow_domains = ['careerlink.vn']
    start_urls = [
            'https://www.careerlink.vn/vieclam/list'
        ]
    custom_settings = {
        'DOWNLOAD_DELAY' : 5,
        'CONCURRENT_REQUESTS_PER_DOMAIN' : 1
    }
    def parse(self, response):
        urls = response.xpath('//a[contains(@class, "job-link clickable-outside")]/@href').getall()
        for url in urls:
            if url not in links:
                url = response.urljoin(url)
                yield scrapy.Request(url=url, callback=self.parse_details)
        next_page_url = response.xpath('//a[contains(@rel, "next")]/@href').get()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            print(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_details(self, response):
        
        data = {}
        data['url'] = response.url
        data['title'] =  response.xpath('//div[contains(@class, "media-body job-title-and-org-name")]/h1/text()').get().strip()

        data['factory'] = response.xpath('//div[contains(@class, "media-body job-title-and-org-name")]/p/a/span/text()').get().strip()

        data['website'] = response.xpath('//a[contains(@itemprop, "url")]/text()').get()

        data['salary'] = response.xpath('//span[contains(@itemprop, "value")]/text()').get().strip()

        m = response.xpath('//ul[contains(@class,"list-unstyled contact-person my-4 rounded-lg")]/li/span/span/text()').getall()
        address = ''
        for i in m:
            address+=', '+i.strip()
        data['address'] = address

        m = response.xpath('//div[contains(@class, "d-flex flex-wrap mt-2")]/div/span/text()').getall()
        data['posting_date'] = m[1].strip()
        data['deadline'] = m[3].strip()

        m = response.xpath('//div[contains(@class,"mb-1 text-body")]/span/text()').get()
        if m is None:
            m = response.xpath('//div[contains(@class,"py-4 location-container")]/div/a/span/text()').getall()
            data['workplace'] = [i.strip() for i in m]
        else: data['workplace'] = m.strip()
        
        data['employment_type'] =  response.xpath('//div[contains(@itemprop, "employmentType")]/text()').get().strip()

        data['qualification'] =  response.xpath('//div[contains(@itemprop, "qualifications")]/text()').get().strip()

        data['experience'] =  response.xpath('//div[contains(@itemprop, "experienceRequirements")]/text()').get().strip()

        data['education'] =  response.xpath('//div[contains(@itemprop, "educationRequirements")]/text()').get().strip()

        data['sex'] =  response.xpath('//*[@id="section-job-description"]/div[3]/div/div[2]/div/div/div[1]/div/div[2]/text()').get().strip()

        data['age'] =  response.xpath('//*[@id="section-job-description"]/div[3]/div/div[2]/div/div/div[2]/div/div/div[2]/text()').get().strip()

        careers =  response.xpath('//span[contains(@itemprop, "occupationalCategory")]/text()').getall()
        data['career'] = [career.strip() for career in careers]


        m = response.xpath('//div[contains(@itemprop, "description")]/p').get()
        data['description'] = re.sub('<.*?>', '', m)
        
        m = response.xpath('//div[contains(@itemprop, "skill")]/p/text()').get()
        data['skill'] = re.sub('<.*?>', '', m)
        mycol.insert_one(data)
        yield data