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

    @property
    def fulltext(self):
        return ' '.join([self.title])

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

def load_documents():
    df0 = pd.read_json('job_news.json')
    doc_id = 0
    for title in df0['title'].tolist():
        if title:
            yield JobSumary(ID=doc_id, title=title)
            doc_id += 1


index = index_documents(load_documents(), Index())
    
print(f'Index contains {len(index.documents)} documents')
search_result = index.search('Kinh doanh Hà Nội', search_type='AND', rank=True)
print(len(search_result))
print(search_result)