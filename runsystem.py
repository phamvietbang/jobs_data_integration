import os

#Chay crawl du lieu tho
# os.system('python runallcrawler.py')
# os.system('python myworks.py')
# os.system('python topcv.py')
#Tich hop cac du lieu
os.system('python ChangeSchemaCleaningData.py')
#Loai bo du lieu trung lap
os.system('python deduplicate.py')
#index du lieu phuc vu tim kiem
os.system('python search.py')