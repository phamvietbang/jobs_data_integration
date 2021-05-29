import scrapy

from ..items import JobCrawlerItem


class A123jobSpider(scrapy.Spider):
    name = '123job'
    allowed_domains = [
        '123job.vn'
    ]
    start_urls = [
        'http://123job.vn/tuyen-dung'
    ]

    custom_settings = {
        'FEED_URI': 'jobs/123job.json'
    }

    def parse(self, response):
        urls = response.xpath(
            '//h2[contains(@class, "job__list-item-title")]/a/@href'
        ).getall()
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(
                url=url,
                callback=self.parse_job
            )

        links = response.xpath(
            '//div[contains(@class, "job__list-pagination")]/ul/li/a/@href'
        ).getall()
        next_page_url = links[6]
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse
            )

    def parse_job(self, response):
        item = JobCrawlerItem()

        item['title'] = response.xpath(
            '//h2[contains(@class, "job-title")]/strong/text()'
        ).get()

        job_desc1 = response.xpath(
            '//div[h2[contains(text(), "Mô tả công việc")]]/div/p/text()'
        ).getall()
        job_desc2 = response.xpath(
            '//div[h2[contains(text(), "Mô tả công việc")]]/div/ul/li/p/text()'
        ).getall()
        job_desc3 = response.xpath(
            '//div[h2[contains(text(), "Mô tả công việc")]]/div/ul/li/text()'
        ).getall()
        item['job_desc'] = [job_desc.strip() for job_desc in job_desc1]
        item['job_desc'].extend([job_desc.strip() for job_desc in job_desc2])
        item['job_desc'].extend([job_desc.strip() for job_desc in job_desc3])

        job_req1 = response.xpath(
            '//div[h2[contains(text(), "Yêu cầu công việc")]]/div/p/text()'
        ).getall()
        job_req2 = response.xpath(
            '//div[h2[contains(text(), "Yêu cầu công việc")]]/div/ul/li/p/text()'
        ).getall()
        job_req3 = response.xpath(
            '//div[h2[contains(text(), "Yêu cầu công việc")]]/div/ul/li/text()'
        ).getall()
        item['job_req'] = [job_req.strip() for job_req in job_req1]
        item['job_req'].extend([job_req.strip() for job_req in job_req2])
        item['job_req'].extend([job_req.strip() for job_req in job_req3])

        job_ben1 = response.xpath(
            '//div[h2[contains(text(), "Quyền lợi chi tiết")]]/div/p/text()'
        ).getall()
        job_ben2 = response.xpath(
            '//div[h2[contains(text(), "Quyền lợi chi tiết")]]/div/ul/li/p/text()'
        ).getall()
        job_ben3 = response.xpath(
            '//div[h2[contains(text(), "Quyền lợi chi tiết")]]/div/ul/li/text()'
        ).getall()
        item['job_ben'] = [job_ben.strip() for job_ben in job_ben1]
        item['job_ben'].extend([job_ben.strip() for job_ben in job_ben2])
        item['job_ben'].extend([job_ben.strip() for job_ben in job_ben3])

        item['salary'] = response.xpath(
            '//div[contains(@class, "item salary")]/b/text()'
        ).get()

        item['com_name'] = response.xpath(
            '//div[contains(@class, "company-review")]/p/text()'
        ).get()

        # com_adds = response.xpath('//div[contains(@class, "marginTop15 fontSize14 fontSize16-xs")]/text()').getall()
        # item['com_add'] = com_adds[1].strip()

        details1 = response.xpath(
            '//div[contain(@class, "item time-expiry-date")]/text()'
        ).getall()

        details2 = response.xpath(
            '//div[contains(@class, "item text-black")]/text()'
        )

        item['job_pos'] = details1

        # item['job_nums_avai'] = details[7].strip("<td>, </td>")

        # item['job_exp'] = response.xpath(
        #     '//div[i[contains(@class, "la la-suitcase")]]/b/text()'
        # ).get()
        #
        # item['location'] = response.xpath(
        #     '//div[i[contains(@class, "la la-map-marker")]]/b/text()'
        # ).get()

        item['url'] = response.url

        item['deadline'] = details2


        yield item