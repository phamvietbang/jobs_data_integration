from selenium import webdriver
import json
import requests

from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
        browser = webdriver.Chrome(r'C:\Users\Administrator\chromedriver_win32\chromedriver.exe',options=options)
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
    # url % page sẽ thay ký tự %d bằng page
    source = requests.get(url % page, headers=HDR)
    # nếu status code khác 200 (200 = OK) thì báo lỗi rồi return
    if source.status_code != 200:
        print("Cannot get products list in page %d! Status code: %d"
              % (page, source.status_code))
        print(source.text)
        return

    soup = BeautifulSoup(source.text, 'html.parser')

    # ghi nhớ số bản ghi hiện tại:
    pre_counter = counter

    # dùng css selector:
    # danh sách jobs trong trang:
    jobs = soup.select("div.row.job")
    for job in jobs:
        try:
            # với mỗi job tìm url và tên job để crawl chi tiết bằng hàm crawl_job()
            job_url = job.select("h4.job-title a")[0].get("href")
            title = job.select("h4.job-title a span")[0].text
            crawl_job(job_url, title)
        except IndexError:
            continue

    # nếu không crawl được thêm job nào thì cút luôn
    # nếu có thì gọi đệ quy crawl trang tiếp theo:
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
        # trong job_info này có nhiều thông tin như hình thức làm việc, chức vụ...
        # nhưng ở đây chỉ lấy tạm lương làm mẫu thôi:
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
            if "Mức lương" in info.find_element(By.TAG_NAME, "strong").text:
                salary = info.find_element(By.TAG_NAME, "span").text

            if "Số lượng cần tuyển" in info.find_element(By.TAG_NAME, "strong").text:
                candidates = info.find_element(By.TAG_NAME, "span").text

            if "Chức vụ" in info.find_element(By.TAG_NAME, "strong").text:
                job_position = info.find_element(By.TAG_NAME, "span").text

            if "Yêu cầu kinh nghiệm" in info.find_element(By.TAG_NAME, "strong").text:
                experience = info.find_element(By.TAG_NAME, "span").text
            if "Yêu cầu giới tính" in info.find_element(By.TAG_NAME, "strong").text:
                gender = info.find_element(By.TAG_NAME, "span").text

        destination = browser.find_element(By.CSS_SELECTOR, "div.text-dark-gray").text
        time_submission = browser.find_element(By.CSS_SELECTOR, "div.text-dark-gray.job-deadline").text
        name_company = browser.find_element(By.CSS_SELECTOR, "div.company-title span a").text
        print(name_company)
        for _, info in enumerate(tin_tuyen_dung):
            tags = info.find_elements_by_tag_name('h2')
            contents = info.find_elements(By.CSS_SELECTOR, "div.content-tab")
            for tag in tags:
                if "MÔ TẢ CÔNG VIỆC" in tag.text:
                    job_description = contents[0].text
                if "YÊU CẦU ỨNG VIÊN" in tag.text:
                    job_requirements = contents[1].text
                if "QUYỀN LỢI ĐƯỢC HƯỞNG" in tag.text:
                    benefit = contents[2].text
    except NoSuchElementException as e:
        # không tìm thấy trường nào thì cút luôn
        print(e)
        return

    # thêm job mới vào biến global results:
    if not salary or not job_description:  # không get được salary thì cút ngay
        return
    result = Job(title, url, name_company, salary, destination, candidates, experience, job_position, gender,
                 time_submission, job_description, job_requirements, benefit).to_json()
    results.append(result)
    if len(results) % 1000 == 0:
        with open(OUTPUT_FILE, "a+", encoding='utf8') as file:
            for job in results:
                json.dump(job, file, ensure_ascii=False)
                file.write("\n")
            file.close()
            results = []
        print(title, url)

    # tăng biến đếm bản ghi lên 1:
    counter += 1
    print("Crawled %d product(s)!" % counter)
    if counter == LIMIT:
        # nếu crawl đủ thì throw exception Enough để thoát nhanh ra hàm main:
        raise Enough()


def main(user, password):
    global counter, browser, results
    # khởi tạo 3 biến global:
    counter = 0
    browser = init_browser(BROWSER)
    results = list()

    # đăng nhập vào topcv để hiện lương đã:
    browser.get(LOGIN_PAGE)
    # dấu # nghĩa là id, . nghĩa là class
    username_textbox, pass_textbox = browser.find_elements(By.CSS_SELECTOR, "#form-login input")[1:3]
    username_textbox.send_keys(user)
    pass_textbox.send_keys(password)
    # click đăng nhập
    browser.find_element(By.CSS_SELECTOR, "#form-login input.btn.btn-topcv-primary.btn-block").click()
    # đợi 5 giây
    WebDriverWait(browser, 5)

    # test thử hiện lương:
    # browser.get(BASE_LINK % 1)
    # print([e.text for e in browser.find_elements_by_css_selector("span.text-highlight")])

    # bắt đầu crawl:
    try:
        crawl_page(BASE_LINK, 1)
    except Enough:
        # crawl đủ rồi:
        print("Completed!")
    except Exception as e:
        print("Cannot complete crawling!")
        print(e)
        # uncomment 2 cái dưới nếu nếu in exception rõ hơn debug cho dễ:
        import traceback
        traceback.print_exc()
    finally:
        pass
        # nếu results không rỗng thì lưu dữ liệu lại:
        # if len(results)%5000 == 0:
        #     print("Saving %d product(s)..." % counter)
        #     with open(OUTPUT_FILE, "w", encoding='utf8') as file:
        #       for job in results:
        #         json.dump(job, file, ensure_ascii=False)
        #         file.write("\n")
        #       file.close()


if __name__ == '__main__':
    # link gốc, thay page = 1, 2, 3... vào %d
    BASE_LINK = "https://www.topcv.vn/tim-viec-lam-moi-nhat?page=%d"
    # trang login topcv
    LOGIN_PAGE = "https://www.topcv.vn/login"
    # user agent để fake trình duyệt cho đỡ bị chặn:
    HDR = {'User-Agent': 'Mozilla/5.0'}
    # tên trình duyệt để truyền vào hàm init_browser() trên kia
    BROWSER = "chrome"
    # limit số bản ghi tối đa crawl:
    LIMIT = 100000
    # thời gian tối đa đợi load javascript
    WAIT_TIME = 10
    # file lưu dữ liệu
    OUTPUT_FILE = "output/20202/topcv_new.json"

    counter = None  # đếm bao nhiêu bản ghi đã crawl
    browser = None  # browser
    results = None  # lưu data tạm thời vào đây
    main("uiui1999vn@gmail.com", "tienanh99")
