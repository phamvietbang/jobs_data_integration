import json
import pandas as pd
pd.read_json

if __name__ == '__main__':
    topcv_data = []
    for line in open('output/topcv.json', 'r', encoding='utf-8'):
        topcv_data.append(json.loads(line))
    with open('output/topcv.json', 'w', encoding='utf-8') as f:
        json.dump(topcv_data, f, ensure_ascii=False)
    mywork_data = []
    for line in open('output/myworks.json', 'r', encoding='utf-8'):
        mywork_data.append(json.loads(line))
    with open('output/myworks.json', 'w', encoding='utf-8') as f:
        json.dump(mywork_data, f, ensure_ascii=False)