from selenium import webdriver
import json
import requests

from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient


myclient = MongoClient("mongodb://localhost:27017/")
mydb = myclient["crawljob"]
mycol = mydb["new_topcv"]


class Enough(Exception):
    pass


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
        browser = webdriver.Chrome('chromedriver.exe',options=options)
    else:
        raise Exception("Browser is not supported!")
    return browser


class Job:
    def __init__(self, title, url, name_company, salary, destination, candidates, experience, job_position, gender,
                 time_submission, job_description, job_requirements, benefit):
        self.title = title
        self.url = url
        self.name_company = name_company
        self.salary = salary
        self.destination = destination
        self.candidates = candidates
        self.experience = experience
        self.job_position = job_position
        self.gender = gender
        self.time_submission = time_submission
        self.job_description = job_description
        self.job_requirements = job_requirements
        self.benefit = benefit

    def to_json(self):
        return {"title": self.title,
                "url": self.url,
                "name_company": self.name_company,
                "salary": self.salary,
                "destination": self.destination,
                "candidates": self.candidates,
                "experience": self.experience,
                "job_position": self.job_position,
                "gender": self.gender,
                "time_submission": self.time_submission,
                "job_description": self.job_description,
                "job_requirements": self.job_requirements,
                "benefit": self.benefit
                }


def crawl_page(url, page=1):
    global counter
    # url % page s??? thay k?? t??? %d b???ng page
    source = requests.get(url % page, headers=HDR)
    # n???u status code kh??c 200 (200 = OK) th?? b??o l???i r???i return
    if source.status_code != 200:
        print("Cannot get products list in page %d! Status code: %d"
              % (page, source.status_code))
        print(source.text)
        return

    soup = BeautifulSoup(source.text, 'html.parser')

    # ghi nh??? s??? b???n ghi hi???n t???i:
    pre_counter = counter

    # d??ng css selector:
    # danh s??ch jobs trong trang:
    jobs = soup.select("div.row.job")
    for job in jobs:
        try:
            # v???i m???i job t??m url v?? t??n job ????? crawl chi ti???t b???ng h??m crawl_job()
            job_url = job.select("h4.job-title a")[0].get("href")
            title = job.select("h4.job-title a span")[0].text
            crawl_job(job_url, title)
        except IndexError:
            continue

    # n???u kh??ng crawl ???????c th??m job n??o th?? c??t lu??n
    # n???u c?? th?? g???i ????? quy crawl trang ti???p theo:
    if pre_counter != counter:
        crawl_page(url, page + 1)
    else:
        raise Enough()


def crawl_job(url, title):
    global counter, browser, results
    print("Crawling %s..." % url)
    browser.get(url)
    try:
        job_info = browser.find_elements(By.CSS_SELECTOR, "#box-info-job div.job-info-item")
        tin_tuyen_dung = browser.find_elements(By.CSS_SELECTOR, "div#col-job-left.col-md-8.col-sm-12")
        # trong job_info n??y c?? nhi???u th??ng tin nh?? h??nh th???c l??m vi???c, ch???c v???...
        # nh??ng ??? ????y ch??? l???y t???m l????ng l??m m???u th??i:
        salary = None
        destination = None
        candidates = None
        job_position = None
        experience = None
        gender = None
        time_submission = None
        job_description = None
        job_requirements = None
        benefit = None
        name_company = None
        for info in job_info:
            if "M???c l????ng" in info.find_element(By.TAG_NAME, "strong").text:
                salary = info.find_element(By.TAG_NAME, "span").text

            if "S??? l?????ng c???n tuy???n" in info.find_element(By.TAG_NAME, "strong").text:
                candidates = info.find_element(By.TAG_NAME, "span").text

            if "Ch???c v???" in info.find_element(By.TAG_NAME, "strong").text:
                job_position = info.find_element(By.TAG_NAME, "span").text

            if "Y??u c???u kinh nghi???m" in info.find_element(By.TAG_NAME, "strong").text:
                experience = info.find_element(By.TAG_NAME, "span").text
            if "Y??u c???u gi???i t??nh" in info.find_element(By.TAG_NAME, "strong").text:
                gender = info.find_element(By.TAG_NAME, "span").text

        destination = browser.find_element(By.CSS_SELECTOR, "div.text-dark-gray").text
        time_submission = browser.find_element(By.CSS_SELECTOR, "div.text-dark-gray.job-deadline").text
        name_company = browser.find_element(By.CSS_SELECTOR, "div.company-title span a").text
        print(name_company)
        for _, info in enumerate(tin_tuyen_dung):
            tags = info.find_elements_by_tag_name('h2')
            contents = info.find_elements(By.CSS_SELECTOR, "div.content-tab")
            for tag in tags:
                if "M?? T??? C??NG VI???C" in tag.text:
                    job_description = contents[0].text
                if "Y??U C???U ???NG VI??N" in tag.text:
                    job_requirements = contents[1].text
                if "QUY???N L???I ???????C H?????NG" in tag.text:
                    benefit = contents[2].text
    except NoSuchElementException as e:
        # kh??ng t??m th???y tr?????ng n??o th?? c??t lu??n
        print(e)
        return

    # th??m job m???i v??o bi???n global results:
    if not salary or not job_description:  # kh??ng get ???????c salary th?? c??t ngay
        return
    result = Job(title, url, name_company, salary, destination, candidates, experience, job_position, gender,
                 time_submission, job_description, job_requirements, benefit).to_json()
    mycol.insert_one(result)
    results.append(result)
    if len(results) % 1000 == 0:
        # with open(OUTPUT_FILE, "a+", encoding='utf8') as file:
        #     for job in results:
        #         json.dump(job, file, ensure_ascii=False)
        #         file.write("\n")
        #     file.close()
            results = []
        # print(title, url)

    # t??ng bi???n ?????m b???n ghi l??n 1:
    counter += 1
    print("Crawled %d product(s)!" % counter)
    if counter == LIMIT:
        # n???u crawl ????? th?? throw exception Enough ????? tho??t nhanh ra h??m main:
        raise Enough()


def main(user, password):
    global counter, browser, results
    # kh???i t???o 3 bi???n global:
    counter = 0
    browser = init_browser(BROWSER)
    results = list()

    # ????ng nh???p v??o topcv ????? hi???n l????ng ????:
    browser.get(LOGIN_PAGE)
    # d???u # ngh??a l?? id, . ngh??a l?? class
    username_textbox, pass_textbox = browser.find_elements(By.CSS_SELECTOR, "#form-login input")[1:3]
    username_textbox.send_keys(user)
    pass_textbox.send_keys(password)
    # click ????ng nh???p
    browser.find_element(By.CSS_SELECTOR, "#form-login input.btn.btn-topcv-primary.btn-block").click()
    # ?????i 5 gi??y
    WebDriverWait(browser, 5)

    # test th??? hi???n l????ng:
    # browser.get(BASE_LINK % 1)
    # print([e.text for e in browser.find_elements_by_css_selector("span.text-highlight")])

    # b???t ?????u crawl:
    try:
        crawl_page(BASE_LINK, 1)
    except Enough:
        # crawl ????? r???i:
        print("Completed!")
    except Exception as e:
        print("Cannot complete crawling!")
        print(e)
        # uncomment 2 c??i d?????i n???u n???u in exception r?? h??n debug cho d???:
        import traceback
        traceback.print_exc()
    finally:
        pass
        # n???u results kh??ng r???ng th?? l??u d??? li???u l???i:
        # if len(results)%5000 == 0:
        #     print("Saving %d product(s)..." % counter)
        #     with open(OUTPUT_FILE, "w", encoding='utf8') as file:
        #       for job in results:
        #         json.dump(job, file, ensure_ascii=False)
        #         file.write("\n")
        #       file.close()


if __name__ == '__main__':
    # link g???c, thay page = 1, 2, 3... v??o %d
    BASE_LINK = "https://www.topcv.vn/tim-viec-lam-moi-nhat?page=%d"
    # trang login topcv
    LOGIN_PAGE = "https://www.topcv.vn/login"
    # user agent ????? fake tr??nh duy???t cho ????? b??? ch???n:
    HDR = {'User-Agent': 'Mozilla/5.0'}
    # t??n tr??nh duy???t ????? truy???n v??o h??m init_browser() tr??n kia
    BROWSER = "chrome"
    # limit s??? b???n ghi t???i ??a crawl:
    LIMIT = 100000
    # th???i gian t???i ??a ?????i load javascript
    WAIT_TIME = 10
    # file l??u d??? li???u
    OUTPUT_FILE = "output/20202/topcv_new.json"

    counter = None  # ?????m bao nhi??u b???n ghi ???? crawl
    browser = None  # browser
    results = None  # l??u data t???m th???i v??o ????y
    main("uiui1999vn@gmail.com", "tienanh99")
