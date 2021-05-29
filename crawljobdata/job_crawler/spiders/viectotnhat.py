from datetime import datetime

import scrapy

from ..items import JobCrawlerItem


class ViectotnhatSpider(scrapy.Spider):
    name = 'viectotnhat'
    allowed_domains = ['viectotnhat.com']
    start_urls = ['http://viectotnhat.com/viec-lam/tim-kiem']

    custom_settings = {
        'FEED_URI': 'jobs/viectotnhat.json'
    }

    def parse(self, response):
        urls = response.xpath('//h3[contains(@class, "job-name margin0")]/a/@href').getall()
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_job)

        next_page_url = response.xpath('//div[contains(@class, "alignCenter marginBottom10 hidden-xs ")]/nav/ul/li['
                                       '5]/a/@href').get()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_job(self, response):
        data = JobCrawlerItem()

        data['title'] = response.xpath('//h1[contains(@class, "marginTop0 fontSize32 font700 title-job")]/text()').get()

        job_desc1 = response.xpath('//div[contains(@class, "mo-ta-cv marginTop20 fontSize16-xs '
                                   'uppercase_first_letter")]/text()').getall()
        job_desc2 = response.xpath('//div[contains(@class, "mo-ta-cv marginTop20 fontSize16-xs '
                                   'uppercase_first_letter")]/li/text()').getall()
        data['job_desc'] = [job_desc.strip() for job_desc in job_desc1]
        data['job_desc'].extend([job_desc.strip() for job_desc in job_desc2])

        job_req1 = response.xpath('//div[contains(@class, "yeu-cau marginTop20 fontSize16-xs '
                                  'uppercase_first_letter")]/text()').getall()
        job_req2 = response.xpath('//div[contains(@class, "yeu-cau marginTop20 fontSize16-xs '
                                  'uppercase_first_letter")]/ul/li/text()').getall()
        data['job_req'] = [job_req.strip() for job_req in job_req1]
        data['job_req'].extend([job_req.strip() for job_req in job_req2])

        job_ben1 = response.xpath('//div[contains(@class, "quyen-loi marginTop20 fontSize16-xs '
                                  'uppercase_first_letter")]/text()').getall()
        job_ben2 = response.xpath('//div[contains(@class, "quyen-loi marginTop20 fontSize16-xs '
                                  'uppercase_first_letter")]/ul/li/text()').getall()
        data['job_ben'] = [job_ben.strip() for job_ben in job_ben1]
        data['job_ben'].extend([job_ben.strip() for job_ben in job_ben2])

        salary = response.xpath('//li[contains(@class, " marginBottom12 marginBottom17-xs paddingLeft30 relative '
                                'fontSize16-xs")]/text()').getall()
        data['salary'] = salary[2].strip()

        data['com_name'] = response.xpath('//h3[contains(@class, "font600 fontSize18 fontSize20-xs  marginBottom10 '
                                          'lineh12")]/text()').get()

        com_adds = response.xpath('//div[contains(@class, "marginTop15 fontSize14 fontSize16-xs")]/text()').getall()
        data['com_add'] = com_adds[1].strip()

        job_poss = response.xpath('//li[contains(@class, "marginBottom12 marginBottom17-xs paddingLeft30 '
                                  'paddingLeft40-pc relative fontSize16-xs")]/text()').getall()
        data['job_pos'] = job_poss[6].strip()

        job_nums_avais = response.xpath(
            '//li[contains(@class, " marginBottom12 marginBottom17-xs paddingLeft30 relative fontSize16-xs")]/span/text()').getall()
        data['job_nums_avai'] = job_nums_avais[2].strip()

        job_exps = response.xpath('//li[contains(@class, " marginBottom12 marginBottom17-xs relative paddingLeft30 '
                                  'fontSize16-xs")]/text()').getall()
        data['job_exp'] = job_exps[2].strip()

        locations = response.xpath(
            '//li[contains(@class, " marginBottom12 marginBottom17-xs paddingLeft30 paddingLeft40-pc relative '
            'fontSize16-xs")]/a/text()').getall()
        data['location'] = locations[0].strip()

        certi = response.xpath(
            '//li[contains(@class, " marginBottom12 marginBottom17-xs relative paddingLeft30 fontSize16-xs")]/text()').getall()
        data['certificate'] = certi[5].strip()

        infos = response.xpath('//div[contains(@class, "ho-so marginTop20 fontSize16-xs")]/ul/li/text()').getall()
        infomations = [info.strip() for info in infos]
        data['info'] = "/".join(infomations)

        data['url'] = response.url
        # data['time_collect'] = datetime.now()

        deadlines = response.xpath(
            '//span[contains(@class, "color-orange2 font400-xs color-black-xs")]/text()').getall()
        data['deadline'] = deadlines[0].strip()
        gender = response.xpath(
            '//li[contains(@class, " marginBottom12 marginBottom17-xs relative paddingLeft30 paddingLeft40-pc fontSize16-xs")]/text()'
        ).getall()
        data['gender'] = gender[2].strip()

        yield data
