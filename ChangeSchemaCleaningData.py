import read_data
import pandas as pd
import os
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["local"]
mycol = mydb["alljob"]

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
                  'position', 'experience', 'working_location', 'degree', 'company_link',
                  'news_link', 'deadline', 'types']
jobsgo['source'] = "jobsgo.vn"
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
# thi???u H??nh th???c l??m vi???c, ID c??ng vi???c, M???c th?????ng
data_job["source"] = "1001vieclam.com"
data_job["crawled_time"] = ""
data_job["news_link"] = data["url"]
data_job["title"] = data["title"]
data_job["salary"] = data["L????ng"]
# data_job["bonus"] = data["M???c th?????ng"]
# data_job["working_form"] = data["H??nh th???c l?? vi???c"]
# data_job["ID_job"] = data["ID c??ng vi???c"]
data_job["number_available"] = ""
data_job["description"] = data["M?? t??? c??ng vi???c"]
data_job["benefits"] = data["Quy???n l???i"]
data_job["working_location"] = data["N??i l??m vi???c"]
data_job["types"] = data["Ng??nh"]
data_job["experience"] = ""
data_job["degree"] = ""
data_job["gender"] = ""
data_job["updated_date"] = ""
data_job["deadline"] = data["Ng??y h???t h???n"]
data_job["requirements"] = data["Y??u c???u c??ng vi???c"]
data_job["company_name"] = data["factory"]
data_job["company_link"] = ""
data_job["company_address"] = ""
datajob3 = pd.DataFrame(data_job)


data = read_data.read_mongo(db='crawljob', collection='careerbuilder')
data_job = dict()
# thi???u H??nh th???c, C???p b???c, Th??ng tin kh??c, jobtags/skill
data_job["source"] = "careerbuilder.vn"
data_job["crawled_time"] = ""
data_job["news_link"] = data["url"]
data_job["title"] = data["title"]
data_job["salary"] = data["L????ng"]
# data_job["working_form"] = data["H??nh th???c"]
# data_job["position"] = data["C???p b???c"]
data_job["number_available"] = ""
data_job["description"] = data["M?? t??? c??ng vi???c"]
data_job["benefits"] = data["Ph??c l???i"]
data_job["working_location"] = data["city"]
data_job["types"] = data["Ng??nh ngh???"]
data_job["experience"] = data["Kinh nghi???m"]
data_job["degree"] = ""
data_job["gender"] = ""
data_job["updated_date"] = ""
data_job["deadline"] = data["H???t h???n n???p"]
data_job["requirements"] = data["Y??u c???u c??ng vi???c"]
data_job["company_name"] = data["factory"]
data_job["company_link"] = ""
data_job["company_address"] = ""
#data_job["other_information"] = data["th??ng tin kh??c"]
# data_job["jobtags"] = data["jobtags/skill"]
datajob4 = pd.DataFrame(data_job)


data = read_data.read_mongo(db='crawljob', collection='vietnamworks')
data_job = dict()
# thi???u K??? N??ng, address (th??nh ph??? tuy???n d???ng)
data_job["source"] = "vietnamworks.com"
data_job["crawled_time"] = ""
data_job["news_link"] = data["url"]
data_job["title"] = data["title"]
data_job["salary"] = data["salary"]
data_job["number_available"] = ""
data_job["description"] = data["M?? T??? C??ng Vi???c"]
data_job["benefits"] = data["Ph??c l???i"]
data_job["working_location"] = data["?????a ??i???m l??m vi???c"]
# data_job["city"] = data["address"]
# data_job["skill"] = data["K??? n??ng"]
data_job["types"] = data["Ng??nh Ngh???"]
data_job["experience"] = ""
data_job["degree"] = ""
data_job["gender"] = ""
data_job["updated_date"] = data["Ng??y ????ng Tuy???n"]
data_job["deadline"] = data["H???n c??n"]
data_job["requirements"] = data["Y??u C???u C??ng Vi???c"]
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
alljob_final2['degree'].replace({"Trung c???p": "Trung c???p - Ngh???", "Ch???ng ch???" : "Ch???ng ch??? chuy??n ng??nh",
                                 "Trung h???c" : "Trung h???c ph??? th??ng", "Thpt" : "Trung h???c ph??? th??ng",
                                 "Th???c s???" : "Th???c s??", "Ti???n s???" : "Ti???n s??", "Cao h???c" : "Th???c s??",
                                 "" : "Kh??ng y??u c???u", "Th???c s?? k??? thu???t ???ng d???ng" : "Th???c s??",
                                 "  ": "Kh??ng y??u c???u"}, inplace=True)
alljob_final2['gender'].replace({"Ch??a c???p nh???t" : "Kh??ng y??u c???u", "" : "Kh??ng y??u c???u",
                                 "0" : "Kh??ng y??u c???u"}, inplace=True)

x = 'Kh??ng x??c ?????nh'
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