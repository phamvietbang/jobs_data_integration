from timing import timing
from index import Index
import pandas as pd
from collections import Counter
from dataclasses import dataclass

from analysis import analyze

@dataclass
class JobSumary:
    ID: int
    title: str
    working_location: str
    company_name: str
    types: str
    @property
    def fulltext(self):
        return ' '.join([self.title, self.working_location, self.company_name, self.types])

    def analyze(self):
        self.term_frequencies = Counter(analyze(self.fulltext))

    def term_frequency(self, term):
        return self.term_frequencies.get(term, 0)

@timing
def index_documents(documents, index):
    for i, document in enumerate(documents):
        index.index_document(document)
        if i % 5000 == 0:
            print(f'Indexed {i} documents', end='\r')
    return index

def load_documents(df):
    df0 = df
    for id in df0.index:
        title = "" if pd.isnull(df0.loc[id, 'title']) else df0.loc[id, 'title']
        working_location = "" if pd.isnull(df0.loc[id, 'working_location']) else df0.loc[id, 'working_location']
        company_name = "" if pd.isnull(df0.loc[id, 'company_name']) else df0.loc[id, 'company_name']
        types = df0.loc[id, 'types']
        types = " ".join(types)
        if title:
            yield JobSumary(ID=id, title=title, working_location=working_location,\
                company_name=company_name, types=types)
