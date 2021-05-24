import read_data
import pandas as pd
import os
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["local"]
mycol = mydb["alljob"]
mycol1 = mydb['link']

job123 = read_data.read_mongo(db='crawljob', collection='123job')
viectotnhat = read_data.read_mongo(db='crawljob', collection='viectotnhat')
viectotnhat = viectotnhat.drop(['info'], axis=1)

jobsgo = read_data.read_mongo(db='crawljob', collection='jobgo')
job_news = read_data.read_mongo(db='crawljob', collection='job_news')

mywork = read_data.read_mongo(db='crawljob', collection='new_mywork')
topcv = read_data.read_mongo(db='crawljob', collection='new_topcv')

job123.columns = ['title', 'description', 'requirements', 'benefits', 'salary',
                  'company_name', 'position', 'number_available', 'experience', 
                  'working_location', 'news_link', 'deadline']
job123['source'] = "123job.vn"
job123['crawled_time'] = ""
job123['degree'] = ""
job123['gender'] = ""
job123['updated_date'] = ""
job123['company_link'] = ""
job123['company_address'] = ""



viectotnhat.columns = ['title', 'description', 'requirements', 'benefits',
                       'salary', 'company_name', 'company_address', 'position',
                       'number_available', 'experience', 'working_location', 
                       'degree', 'news_link', 'deadline']
viectotnhat['source'] = "viectotnhat.com"
viectotnhat['crawled_time'] = ""
viectotnhat['gender'] = ""
viectotnhat['updated_date'] = ""
viectotnhat['company_link'] = ""



jobsgo.columns = ['title', 'description', 'requirements', 'benefits', 
                  'salary', 'company_name', 'company_address', 
                  'position', 'experience', 'degree', 'company_link',
                  'news_link', 'deadline', 'types']
jobsgo['source'] = "jobsgo.vn"
jobsgo['working_location'] = ""
jobsgo['gender'] = ""
jobsgo['updated_date'] = ""
jobsgo['crawled_time'] = ""
jobsgo['number_available'] = ""



job1 = pd.concat([job123, viectotnhat], ignore_index=True)
alljob1 = pd.concat([job1, jobsgo], ignore_index=True)
alljob2 = pd.concat([alljob1, job_news], ignore_index=True)

mywork.columns = ['title', 'news_link', 'company_name', 'salary', 'working_location',
                  'number_available', 'experience', 'position', 'gender',
                  'deadline', 'description', 'requirements', 'benefits']
mywork['source'] = 'mywork.com.vn'

alljob3 = pd.concat([alljob2, mywork], ignore_index=True)
alljob3.info()


topcv.columns = ['title', 'news_link', 'company_name', 'salary', 'working_location', 'number_available',
                 'experience', 'position', 'gender', 'deadline', 'description',
                 'requirements', 'benefits']
topcv['source'] = 'topcv.vn'


alljob4 = pd.concat([alljob3, topcv], ignore_index=True)
alljob4.info()

data = read_data.read_mongo(db='crawljob', collection='1001vieclam')
data_job = dict()
# thiếu Hình thức làm việc, ID công việc, Mức thưởng
data_job["source"] = "1001vieclam.com"
data_job["crawled_time"] = ""
data_job["news_link"] = data["url"]
data_job["title"] = data["title"]
data_job["salary"] = data["Lương"]
# data_job["bonus"] = data["Mức thưởng"]
# data_job["working_form"] = data["Hình thức là việc"]
# data_job["ID_job"] = data["ID công việc"]
data_job["number_available"] = ""
data_job["description"] = data["Mô tả công việc"]
data_job["benefits"] = data["Quyền lợi"]
data_job["working_location"] = data["Nơi làm việc"]
data_job["types"] = data["Ngành"]
data_job["experience"] = ""
data_job["degree"] = ""
data_job["gender"] = ""
data_job["updated_date"] = ""
data_job["deadline"] = data["Ngày hết hạn"]
data_job["requirements"] = data["Yêu cầu công việc"]
data_job["company_name"] = data["factory"]
data_job["company_link"] = ""
data_job["company_address"] = ""
datajob3 = pd.DataFrame(data_job)


data = read_data.read_mongo(db='crawljob', collection='careerbuilder')
data_job = dict()
# thiếu Hình thức, Cấp bậc, Thông tin khác, jobtags/skill
data_job["source"] = "careerbuilder.vn"
data_job["crawled_time"] = ""
data_job["news_link"] = data["url"]
data_job["title"] = data["title"]
data_job["salary"] = data["Lương"]
# data_job["working_form"] = data["Hình thức"]
# data_job["position"] = data["Cấp bậc"]
data_job["number_available"] = ""
data_job["description"] = data["Mô tả công việc"]
data_job["benefits"] = data["Phúc lợi"]
data_job["working_location"] = data["city"]
data_job["types"] = data["Ngành nghề"]
data_job["experience"] = data["Kinh nghiệm"]
data_job["degree"] = ""
data_job["gender"] = ""
data_job["updated_date"] = ""
data_job["deadline"] = data["Hết hạn nộp"]
data_job["requirements"] = data["Yêu cầu công việc"]
data_job["company_name"] = data["factory"]
data_job["company_link"] = ""
data_job["company_address"] = ""
#data_job["other_information"] = data["thông tin khác"]
# data_job["jobtags"] = data["jobtags/skill"]
datajob4 = pd.DataFrame(data_job)


data = read_data.read_mongo(db='crawljob', collection='vietnamworks')
data_job = dict()
# thiếu Kỹ Năng, address (thành phố tuyển dụng)
data_job["source"] = "vietnamworks.com"
data_job["crawled_time"] = ""
data_job["news_link"] = data["url"]
data_job["title"] = data["title"]
data_job["salary"] = data["salary"]
data_job["number_available"] = ""
data_job["description"] = data["Mô Tả Công Việc"]
data_job["benefits"] = data["Phúc lợi"]
data_job["working_location"] = data["Địa điểm làm việc"]
# data_job["city"] = data["address"]
# data_job["skill"] = data["Kỹ năng"]
data_job["types"] = data["Ngành Nghề"]
data_job["experience"] = ""
data_job["degree"] = ""
data_job["gender"] = ""
data_job["updated_date"] = data["Ngày Đăng Tuyển"]
data_job["deadline"] = data["Hạn còn"]
data_job["requirements"] = data["Yêu Cầu Công Việc"]
data_job["company_name"] = data["factory"]
data_job["company_link"] = ""
data_job["company_address"] = ""
datajob5  = pd.DataFrame(data_job)

alljob41 = pd.concat([alljob4, datajob3], ignore_index=True)
datajob6 = pd.concat([datajob4, datajob5], ignore_index=True)
alljob_final = pd.concat([alljob41, datajob6], ignore_index=True)
alljob_final.info()
alljob_final1 = alljob_final.dropna(subset=['title', 'company_name', 'salary'])
alljob_final1.info()

alljob_final2 = alljob_final1.drop(['crawled_time', 'updated_date'], axis=1)
# alljob_final2 = alljob_final2.drop(['update_date'], axis=1)

alljob_final2['title'] = alljob_final2['title'].str.upper()
alljob_final2['company_name'] = alljob_final2['company_name'].str.upper()
alljob_final2['degree'] = alljob_final2['degree'].str.capitalize()
alljob_final2['degree'].replace({"Trung cấp": "Trung cấp - Nghề", "Chứng chỉ" : "Chứng chỉ chuyên ngành",
                                 "Trung học" : "Trung học phổ thông", "Thpt" : "Trung học phổ thông",
                                 "Thạc sỹ" : "Thạc sĩ", "Tiến sỹ" : "Tiến sĩ", "Cao học" : "Thạc sĩ",
                                 "" : "Không yêu cầu", "Thạc sĩ kỹ thuật ứng dụng" : "Thạc sĩ",
                                 "  ": "Không yêu cầu"}, inplace=True)
alljob_final2['gender'].replace({"Chưa cập nhật" : "Không yêu cầu", "" : "Không yêu cầu",
                                 "0" : "Không yêu cầu"}, inplace=True)

x = 'Không xác định'
alljob_final2['types'] = alljob_final2['types'].fillna(x)
if os.path.exists("list_types.txt"):
  os.remove("list_types.txt")
list_types = []
for i in alljob_final2.index:
  if len(alljob_final2.loc[int(i)]['types']) != 0:
    if type(alljob_final2.loc[int(i)]['types']) != type(list()):
      x = []
      x.append(alljob_final2.loc[int(i)]['types'])
      alljob_final2.loc[int(i)]['types'] = x
    for j in alljob_final2.loc[int(i)]['types']:
      if j not in list_types:
        list_types.append(j)


with open("list_types.txt", mode="w", encoding='utf-8') as f:
  for i in list_types:
    f.write(i + "\n")

# alljob_final2.to_json('alljob1.json', orient='records')
mycol.insert(alljob_final2.to_dict('records'))
link = alljob_final2['news_link']
with open("./crawljobdata/crawljobdata/spiders/link.txt", mode="w", encoding='utf-8') as f:
  for i in link:
    f.write(i + "\n")