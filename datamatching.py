# -*- coding: utf-8 -*-
"""DataMatching1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MAu6W4i7IeQDocMOY4-pTHYOHFRbZ04y
"""

# !pip install recordlinkage

import pandas as pd
import recordlinkage

alljob = pd.read_json('')
alljob = alljob.fillna('')
alljob.info()

def duplicateData(dataframe, list_drop_data):
  dupe_indexer = recordlinkage.Index()
  dupe_indexer.sortedneighbourhood(left_on='title')
  dupe_candidate_links = dupe_indexer.index(dataframe)
  print('Candidate: {}'.format(len(dupe_candidate_links)))

  compare_dupes = recordlinkage.Compare()
  compare_dupes.string('title', 'title', threshold=0.85, label='title')
  compare_dupes.string('company_name', 'company_name', threshold=0.95, label='company_name')
  compare_dupes.string('position', 'position', threshold=0.8, label='position')
  compare_dupes.string('working_location', 'working_location', threshold=0.8, label='location')
  dupe_features = compare_dupes.compute(dupe_candidate_links, dataframe)

  potential_dupes = dupe_features[dupe_features.sum(axis=1) > 2].reset_index()
  potential_dupes['Score'] = potential_dupes.loc[:, ].sum(axis=1)
  potential_dupes = potential_dupes[potential_dupes['company_name'] > 0.0]
  potential_dupes = potential_dupes[potential_dupes['title'] > 0.0]

  for i in potential_dupes['level_1']:
    if i not in list_drop_data:
      list_drop_data.append(i)

list_drop = []
duplicateData(alljob, list_drop)
print("Số bản ghi trùng lặp: {}".format(len(list_drop)))

for i in list_drop:
  alljob = alljob.drop(i)
alljob.info()

alljob.to_json('')