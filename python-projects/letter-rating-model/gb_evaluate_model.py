from pymongo import MongoClient
import json
import pandas as pd

with open("../letter-preprocess/secrets.json", 'r') as f:
    info = json.load(f)

mongo_host = "mongodb://{}:{}@{}:{}".format(info['mongo_info']['user'],
                                                    info['mongo_info']['password'],
                                                    info['host'],
                                                    info['mongo_info']['port'])

mongo = MongoClient(mongo_host)
db = mongo['letter_db']
posts = db.posts

data = []

for post in posts.find():
    data.append([post['content'], post['target']])
    
df = pd.DataFrame(data, columns=['content', 'target'])

from keras.preprocessing.text import Tokenizer
from sklearn.model_selection import train_test_split

train_x, test_x, train_y, test_y = train_test_split(df['content'], df['target'], 
                                                    test_size=0.2, random_state=121)

tokenizer = Tokenizer(num_words=10000)
tokenizer.fit_on_texts(list(train_x))

one_hot_train_x = tokenizer.texts_to_matrix(train_x, mode='binary')
one_hot_test_x = tokenizer.texts_to_matrix(test_x, mode='binary')

from keras.utils.np_utils import to_categorical

one_hot_train_y = to_categorical(train_y)
one_hot_test_y = to_categorical(test_y)

x_val = one_hot_train_x[:1000]
partial_x_train = one_hot_train_x[1000:]

y_val = one_hot_train_y[:1000]
partial_y_train = one_hot_train_y[1000:]

from keras import models, layers

model = models.Sequential()
model.add(layers.Dense(64, activation='relu', input_shape=(10000,)))
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(2, activation='softmax'))

model.compile(optimizer='rmsprop',
             loss='categorical_crossentropy',
             metrics=['accuracy'])

history = model.fit(partial_x_train,
                   partial_y_train,
                   epochs=8,
                   batch_size=512,
                   validation_data=(x_val, y_val))

results = model.evaluate(one_hot_test_x, one_hot_test_y)
gb_result = {"loss": results[0],
            "accuracy": results[1],
            "train": len(train_x),
            "test": len(test_x)}

with open('output/gb_result.json', 'w', encoding='utf-8') as f:
    json.dump(gb_result, f, indent="\t")

model.save('output/gb_evaluate_model')

import pickle

with open('output/gb_evaluate_tk.pkl', 'wb') as f:
    pickle.dump(tokenizer, f)
    