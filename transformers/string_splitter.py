import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class StringSplitter(BaseEstimator, TransformerMixin):
    def __init__(self, max_width=''):
        self.max_width = max_width
        self.tags = {}

    def fit(self, words, y=None):
        return self

    def transform(self, words):
        x = np.array(words, dtype=f'U{self.max_width}')
        y = x.view('U1').view(np.uint32).reshape((x.size, -1))
        return pd.DataFrame(y)


if __name__ == '__main__':
    data = [u'в 1905 году'] + u'Определение частей речи работает не так как задумывалось'.split()
    print(data)
    res = StringSplitter().transform(data)
    print(res)
    print(res.shape)
