import scrapy
import selenium
import sys
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from selenium import webdriver
from pymongo import MongoClient

myclient = MongoClient("mongodb://localhost:27017/")
mydb = myclient["crawljob"]
mycol = mydb["vietnamworks"]

def init_browser(type):
    if type == "chrome":
        # headless chrome
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('disable-web-security')
        options.add_argument('allow-running-insecure-content')
        options.add_argument('disable-extensions')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--log-level=3')
        options.add_argument('--silent')
        browser = webdriver.Chrome(options=options,
                                   executable_path='chromedriver.exe')
    else:
        raise Exception("Browser is not supported!")
    return browser


class vietnamworks(scrapy.Spider):
    name = 'vietnamworks'
    allow_domains = ['vietnamworks.com']
    start_urls = [
        'https://www.vietnamworks.com/tim-viec-lam/tat-ca-viec-lam?filtered=true'
    ]
    
    def __init__(self):
        HDR = {'User-Agent': 'Mozilla/5.0'}
        BROWSER = "chrome"
        self.brow = init_browser(BROWSER)
        self.brow.get("https://secure.vietnamworks.com/login/en?client_id=3&utm_source=&utm_medium=Header")
        self.brow.find_elements(By.CSS_SELECTOR, "#form-login input")[1].send_keys("superpower99x99@gmail.com")
        self.brow.find_elements(By.CSS_SELECTOR, "#form-login input")[2].send_keys("K62cnttdhbkhn")
        # click đăng nhập
        self.brow.find_element(By.CSS_SELECTOR, "#form-login input#button-login").click()

        # đợi 5 giây
        WebDriverWait(self.brow, 5)
        self.brow.get("https://www.vietnamworks.com/tim-viec-lam/tat-ca-viec-lam?filtered=true")

    def parse(self, response):

        while True:
            element = self.brow.find_elements_by_xpath('//a[contains(text(), ">")]')
            urls = self.brow.find_elements_by_xpath('//a[contains(@class, "job-title")]')
            for url in urls:
                url = response.urljoin(url.get_attribute('href'))
                yield scrapy.Request(url=url, cookies=self.brow.get_cookies(), callback=self.parse_details)
            try:
                element[0].click()
            except:
                break

        self.brow.close()

    # yield scrapy.Request(callback=self.parse)

    def parse_details(self, response):

        data = {}
        data['url'] = response.url
        data['title'] = response.xpath('//h1[contains(@class, "job-title")]/text()').get().strip()
        data['factory'] = response.xpath('//div[contains(@class, "col-sm-12 company-name")]/a/text()').get().strip()
        data['salary'] = response.xpath('//span[contains(@class, "salary")]/strong/text()').get().strip()
        data['Hạn còn'] = response.xpath('//span[contains(@class, "expiry gray-light")]/text()').get().strip()
        m = response.xpath('//span[contains(text(),"Ngày Đăng Tuyển")]')
        n = m.xpath('string(following-sibling::span)').get()
        if n is not None:
            data['Ngày Đăng Tuyển'] = n.strip()
        else:
            data['Ngày Đăng Tuyển'] = ''

        m = response.xpath('//span[contains(text(),"Cấp Bậc")]')
        n = m.xpath('string(following-sibling::span)').get()
        if n is not None:
            data['Cấp Bậc'] = n.strip()
        else:
            data['Cấp Bậc'] = ''

        m = response.xpath('//span[contains(@class, "content")]/a/text()').getall()
        m = [i.strip() for i in m]
        data['Ngành Nghề'] = m

        m = response.xpath('//span[contains(text(),"Kỹ Năng")]')
        n = m.xpath('string(following-sibling::span)').get()
        if n is not None:
            data['Kỹ Năng'] = n.strip()
        else:
            data['Kỹ Năng'] = ''

        m = response.xpath('//a[contains(@itemprop,"address")]/text()').getall()
        address = ''
        for i in m:
            address += ', ' + i.strip()
        data['address'] = address

        m = response.xpath('//div[contains(@class,"benefit-name col-xs-11")]/text()').getall()
        m = [i.strip() for i in m]
        data['Phúc lợi'] = m
        m = response.xpath('//h2[contains(text(),"Mô Tả Công Việc")]')
        n = m.xpath('string(following-sibling::div)').get()
        if n is not None:
            data['Mô Tả Công Việc'] = n.strip()
        else:
            data['Mô Tả Công Việc'] = ''
        m = response.xpath('//h2[contains(text(),"Yêu Cầu Công Việc")]')
        n = m.xpath('string(following-sibling::div)').get()
        if n is not None:
            data['Yêu Cầu Công Việc'] = n.strip()
        else:
            data['Yêu Cầu Công Việc'] = ''
        data['Địa điểm làm việc'] = response.xpath(
            '//div[contains(@class,"location-name col-xs-11")]/text()').get().strip()
        mycol.insert_one(data)
        yield data