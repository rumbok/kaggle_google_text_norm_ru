from loaders.loading import load_train, load_batch, load_test
from pipeline import transform_chain
import gc
import os
from datetime import datetime
import csv
import pandas as pd
from tqdm import tqdm


SUBM_PATH = r'../input/norm_challenge_ru'
INPUT_PATH = r'../input/norm_challenge_ru'
DATA_INPUT_PATH = r'../input/norm_challenge_ru/ru_with_types'


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


x_test = load_test(INPUT_PATH)
x_test['prev_prev'] = x_test['before'].shift(2)
x_test['prev'] = x_test['before'].shift(1)
x_test['next'] = x_test['before'].shift(-1)
x_test['next_next'] = x_test['before'].shift(-2)
x_test = x_test.fillna('')
test_values = set(x_test['before'].str.lower())

for x_train in load_batch(columns=['class', 'before', 'after'],
                          batch_size=10,
                          input_path=DATA_INPUT_PATH):
    # x_train['prev_prev'] = x_train['before'].shift(2)
    x_train['prev'] = x_train['before'].shift(1)
    x_train['next'] = x_train['before'].shift(-1)
    # x_train['next_next'] = x_train['before'].shift(1)
    x_train = x_train.fillna('')
    x_train = x_train[x_train['before'].str.lower().isin(test_values)]

    y_train = x_train['after']
    del x_train['after']

transform_chain.fit(x_train, y_train)

del x_train, y_train
gc.collect()

del test_values

predicts = []
for x_i in tqdm(chunker(x_test, 30000), 'test', len(x_test)//100000):
    predicts.append(transform_chain.transform(x_i))

predict = pd.concat(predicts)
# predict = transform_chain.transform(x_test)

predict['id'] = predict['sentence_id'].map(str) + '_' + predict['token_id'].map(str)
del predict['before']
del predict['sentence_id']
del predict['token_id']

predict.to_csv(os.path.join(SUBM_PATH, f'ru_predict_{datetime.now().strftime("%Y-%m-%d-%H-%M")}.csv'),
               quoting=csv.QUOTE_NONNUMERIC,
               index=False,
               columns=['id', 'after'])
