import re
import string
from pyvi import ViTokenizer

STOPWORDS = set(['bị','bởi','cả','các','cái','cần','càng','chỉ','chiếc','cho','chứ','chưa','chuyện','có','có_thể','cứ','của','cùng','cũng','đã','đang','đây','để','đến_nỗi','đều','điều','do','đó','được','dưới','gì','khi','không','là','lại','lên','lúc','mà','mỗi','một_cách','này','nên','nếu','ngay','nhiều','như','nhưng','những','nơi','nữa','phải','qua','ra','rằng','rằng','rất','rất','rồi','sau','sẽ','so','sự','tại','theo','thì','trên','trước','từ','từng','và','vẫn','vào','vậy','vì','việc','với','vừa'])
PUNCTUATION = re.compile('[%s]' % re.escape(string.punctuation))

def tokenize(text):
    text = ViTokenizer.tokenize(text)
    return text.split()

def lowercase_filter(tokens):
    return [token.lower() for token in tokens]

def punctuation_filter(tokens):
    return [PUNCTUATION.sub('', token) for token in tokens]

def stopword_filter(tokens):
    return [token for token in tokens if token not in STOPWORDS]

def analyze(text):
    tokens = tokenize(text)
    tokens = lowercase_filter(tokens)
    tokens = punctuation_filter(tokens)
    tokens = stopword_filter(tokens)

    return [token for token in tokens if token]
