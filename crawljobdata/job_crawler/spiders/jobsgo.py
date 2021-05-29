import scrapy

from ..items import JobCrawlerItem


class JobsgoSpider(scrapy.Spider):
    name = 'jobsgo'
    allowed_domains = [
        'jobsgo.vn'
    ]
    start_urls = [
        'http://jobsgo.vn/viec-lam.html'
    ]

    custom_settings = {
        'FEED_URI': 'jobs/jobsgo.json'
    }

    def parse(self, response):
        urls = response.xpath(
            '//div[contains(@class, "h3")]/a/@href'
        ).getall()
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(
                url=url,
                callback=self.parse_job
            )

        next_page_url = response.xpath(
            '//li[contains(@class, "next")]/a/@href'
        ).get()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse
            )

    def parse_job(self, response):
        item = JobCrawlerItem()

        item['title'] = response.xpath(
            '//h1[contains(@class, "media-heading text-semibold")]/text()'
        ).get()

        job_desc1 = response.xpath(
            '//div[h5[contains(text(), "Mô tả công việc")]]/div/p/text()'
        ).getall()
        job_desc2 = response.xpath(
            '//div[h5[contains(text(), "Mô tả công việc")]]/div/p/span/text()'
        ).getall()
        job_desc3 = response.xpath(
            '//div[h5[contains(text(), "Mô tả công việc")]]/div/ul/li/text()'
        ).getall()
        job_desc4 = response.xpath(
            '//div[h5[contains(text(), "Mô tả công việc")]]/div/ul/li/span/text()'
        ).getall()
        job_desc5 = response.xpath(
            '//div[h5[contains(text(), "Mô tả công việc")]]/div//div/p/text()'
        ).getall()
        item['job_desc'] = job_desc1
        item['job_desc'].extend(job_desc2)
        item['job_desc'].extend(job_desc3)
        item['job_desc'].extend(job_desc4)
        item['job_desc'].extend(job_desc5)

        job_req1 = response.xpath(
            '//div[h5[contains(text(), "Yêu cầu công việc")]]/div/p/text()'
        ).getall()
        job_req2 = response.xpath(
            '//div[h5[contains(text(), "Yêu cầu công việc")]]/div/p/span/text()'
        ).getall()
        job_req3 = response.xpath(
            '//div[h5[contains(text(), "Yêu cầu công việc")]]/div/ul/li/text()'
        ).getall()
        job_req4 = response.xpath(
            '//div[h5[contains(text(), "Yêu cầu công việc")]]/div/ul/li/span/text()'
        ).getall()
        job_req5 = response.xpath(
            '//div[h5[contains(text(), "Yêu cầu công việc")]]/div/div/p/text()'
        ).getall()
        item['job_req'] = job_req1
        item['job_req'].extend(job_req2)
        item['job_req'].extend(job_req3)
        item['job_req'].extend(job_req4)
        item['job_req'].extend(job_req5)

        job_ben1 = response.xpath(
            '//div[h5[contains(text(), "Quyền lợi được hưởng")]]/div/p/text()'
        ).getall()
        job_ben2 = response.xpath(
            '//div[h5[contains(text(), "Quyền lợi được hưởng")]]/div/p/span/text()'
        ).getall()
        job_ben3 = response.xpath(
            '//div[h5[contains(text(), "Quyền lợi được hưởng")]]/div/ul/li/text()'
        ).getall()
        job_ben4 = response.xpath(
            '//div[h5[contains(text(), "Quyền lợi được hưởng")]]/div/ul/li/span/text()'
        ).getall()
        job_ben5 = response.xpath(
            '//div[h5[contains(text(), "Quyền lợi được hưởng")]]/div/div/p/text()'
        ).getall()
        item['job_ben'] = job_ben1
        item['job_ben'].extend(job_ben2)
        item['job_ben'].extend(job_ben3)
        item['job_ben'].extend(job_ben4)
        item['job_ben'].extend(job_ben5)

        item['salary'] = response.xpath(
            '//span[contains(@class, "saraly text-bold text-green")]/text()'
        ).get()

        item['com_name'] = response.xpath(
            '//h2[contains(@class, "media-heading text-grey-600 text-semibold text-uppercase text-bold mb-5")]/text()'
        ).get()

        com_adds = response.xpath(
            '//div[contains(@class, "company-info text-grey")]/p/text()'
        ).getall()
        item['com_add'] = com_adds[0]

        job_poss = response.xpath(
            '//span[contains(@itemprop, "name")]/text()'
        ).getall()
        item['job_pos'] = job_poss[2]

        job_exps = response.xpath(
            '//div[contains(@class, "box-jobs-info")]/p/text()'
        ).getall()
        item['job_exp'] = job_exps[3]

        location = response.xpath(
            '//div[contains(@class, "box-jobs-info")]/div/div/p/a/text()'
        ).get()
        item['location']  = location

        item['certificate'] = job_exps[2]

        item['info'] = com_adds[1]

        item['url'] = response.url

        item['deadline'] = response.xpath(
            '//span[contains(@class, "deadline text-bold text-orange")]/text()'
        ).get() + "ngày nữa."

        types = response.xpath(
            '//a[contains(@class, "btn btn-xs btn-default")]/text()'
        ).getall()
        types.pop()
        item['types'] = types


        yield item