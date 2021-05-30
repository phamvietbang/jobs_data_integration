import os
# os.system('python runallcrawler.py')
os.system('python ChangeSchemaCleaningData.py')
os.system('python deduplicate.py')
os.system('python search.py')