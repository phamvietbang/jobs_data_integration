Create output folder named 'output' here to save data after finished crawl topcv and mywork
add path to chromedriver.exe in your computer ( line 30 topcv.py)
install requirements.txt if nessesary
After crawl topcv and mywworks. output folder contains 2 file topcv.json and myworks.json
You must to convert them(run python map_data.py) in order to read its by (pd.read_json)
