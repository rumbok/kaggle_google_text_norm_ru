import pandas as pd
import numpy as np
from sklearn.base import TransformerMixin, BaseEstimator
from tqdm import tqdm


class LettersTransformer(TransformerMixin, BaseEstimator):
    def __init__(self, by_class=False):
        self.by_class = by_class

    def fit(self, X, y=None, *args, **kwargs):
        return self

    def transform(self, X: pd.DataFrame, y=None, *args, **kwargs):
        data = []
        for (word, cls) in tqdm(zip(X['before'], X['class']), f'{self.__class__.__name__} transform', total=len(X)):
            w = word.replace(" ", "").replace(".", "")
            if (self.by_class and cls == 'LETTERS') or (not self.by_class and w.isupper()):
                data.append(' '.join(list(w.lower())))
            else:
                data.append(None)

        if 'after' in X.columns:
            return X.assign(after=X['after'].combine_first(pd.Series(data, index=X.index)))
        else:
            return X.assign(after=data)


if __name__ == '__main__':
    df = pd.DataFrame.from_dict({"КПСС": "к п с с",
                                 "PCM": "p c m",
                                 "Н. К.": "н к"}, orient='index')\
        .reset_index()\
        .rename(columns={'index': 'before', 0: 'actual'})

    res = LettersTransformer().transform(df)
    print('translit', np.mean(res['actual']==res['after']))
    print(res)
