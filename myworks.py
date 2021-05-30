import json

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

myclient = MongoClient("mongodb://localhost:27017/")
mydb = myclient["crawljob"]
mycol = mydb["new_mywork"]


class Enough(Exception):
    # raise this exception when you've already crawled enough
    pass

BASE_LINK = "https://mywork.com.vn/tuyen-dung?page=%d"
PREFIX = "https://mywork.com.vn"
HDR = {'User-Agent': 'Mozilla/5.0'}
BROWSER = "chrome"
LIMIT = 100000
WAIT_TIME = 2
OUTPUT_FILE = "output/myworks.json"

counter = None
browser = None
results = None


class Job:

    def __init__(self, title, url, name_company, salary, destination, candidates, experience, job_position, gender,
                 time_submission,
                 job_description, job_requirements, benefit):
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
                "benefit": self.benefit, }



def crawl_job(job):
    job.url = PREFIX + job.url
    global counter, results
    print("Crawling %s..." % job.url)
    source = requests.get(job.url, headers=HDR)
    if source.status_code != 200:
        print("Cannot get product details from %s! Status code: %d"
              % (job.url, source.status_code))
        print(source.text)
        return
    soup = BeautifulSoup(source.text, 'html.parser')
    try:
        job.candidates = soup.select("div.jsx-2246677448.detail-01-table-td.ex-sl div")[0].text
    except IndexError:
        pass
    try:
        job.job_position = soup.select("div.jsx-2246677448.detail-01-table-td.ex-cb div")[0].text
    except IndexError:
        pass
    try:
        job.gender = soup.select("div.jsx-2246677448.detail-01-table-td.ex-gt div")[0].text
    except IndexError:
        pass
    try:
        job.time_submission = soup.select("div.jsx-2246677448.detail-01-table-td.ex-han-nop div")[0].text
    except IndexError:
        pass
    try:
        job.name_company = soup.select("div.detail-01 a")[0].text
        print(job.name_company)
    except IndexError:
        pass

    descs = soup.select("div.detail-01-row-block")
    for desc in descs:
        try:
            if "MÔ TẢ CÔNG VIỆC" in desc.select("div.detail-01-row-ttl")[0].text.upper():
                job.job_description = desc.select("p")[0].text
            elif "YÊU CẦU CÔNG VIỆC" in desc.select("div.detail-01-row-ttl")[0].text.upper():
                job.job_requirements = desc.select("p")[0].text
            elif "QUYỀN LỢI ĐƯỢC HƯỞNG" in desc.select("div.detail-01-row-ttl")[0].text.upper():
                job.benefit = desc.select("p")[0].text
        except IndexError:
            pass
    infos = soup.select("div.jsx-3495269652.contact-01-info div")
    for info in infos:
        try:
            if "ĐỊA CHỈ" in info.select("span b")[0].text.upper():
                job.destination = info.select("span")[1].text
                break
        except IndexError:
            pass
    mycol.insert_one(job.to_json())
    results.append(job.to_json())
    # print(job.to_json())
    if len(results) % 1000 == 0:
        # with open(OUTPUT_FILE, "a+", encoding='utf8') as file:
        #     for job in results:
        #         json.dump(job, file, ensure_ascii=False)
        #         file.write("\n")
        #     file.close()
            results = []
    counter += 1
    print("Crawled %d job(s)!" % counter)
    if counter == LIMIT:
        raise Enough()


def crawl_page(url, page=1):
    global counter
    source = requests.get(url % page, headers=HDR)
    if source.status_code != 200:
        print("Cannot get products list in page %d! Status code: %d"
              % (page, source.status_code))
        print(source.text)
        return
    soup = BeautifulSoup(source.text, 'html.parser')
    pre_counter = counter
    jobs = soup.select("li.jobslist-01-li")
    for job in jobs:
        j = Job(None, None, None, None, None, None, None, None, None, None, None, None, None)
        try:
            a = job.select("div.jobslist-01-row-ttl a")[0]
            j.title = a.get("title")
            j.url = a.get("href")
        except IndexError:
            continue
        try:
            j.salary = job.select("li.col-12.col-sm-6.col-md-6.col-lg-6.ex-salary span.ml-1")[0].text
        except IndexError:
            pass
        try:
            j.experience = job.select("li.col-12.col-sm-6.col-md-6.col-lg-6.ex-experi.d-pc span.ml-1")[0].text
        except IndexError:
            pass
        crawl_job(j)
    if pre_counter != counter:
        crawl_page(url, page + 1)
    else:
        raise Enough()


def main():
    global counter, browser, results
    counter = 0
    results = []
    try:
        crawl_page(BASE_LINK, 1)
    except Enough:
        print("Completed!")
    except Exception as e:
        print("Cannot complete crawling!")
        print(e)
        import traceback
        traceback.print_exc()
    finally:
        pass
        # if results:
        #     print("Saving %d product(s)..." % counter)
        #     with open(OUTPUT_FILE, "w", encoding="utf8") as file:
        #         json.dump(results, file)


if __name__ == "__main__":
    main()
