from pymongo import MongoClient
import json
import pandas as pd
import numpy as np

with open("../letter-preprocess/secrets.json", 'r') as f:
    info = json.load(f)

mongo_host = "mongodb://{}:{}@{}:{}".format(info['mongo_info']['user'],
                                                    info['mongo_info']['password'],
                                                    info['host'],
                                                    info['mongo_info']['port'])

mongo = MongoClient(mongo_host)
db = mongo['rating_db']
posts = db.posts

data = []

for post in posts.find():
    data.append([post['content'], post['target']])
    
df = pd.DataFrame(data, columns=['content', 'target'])

from keras.preprocessing.text import Tokenizer
from sklearn.model_selection import train_test_split

train_x, test_x, train_y, test_y = train_test_split(df['content'], df['target'], test_size=0.2, random_state=121)

tokenizer = Tokenizer(num_words=10000)
tokenizer.fit_on_texts(list(train_x))

one_hot_train_x = tokenizer.texts_to_matrix(train_x, mode='binary')
one_hot_test_x = tokenizer.texts_to_matrix(test_x, mode='binary')

label_dict = {1.0 : 0, 1.5 : 1, 2.0 : 2, 2.5 : 3, 
              3.0 : 4, 3.5 : 5, 4.0 : 6, 4.5 : 7, 5.0 : 8}

with open('output/rating_label.json', 'w', encoding='utf-8') as f:
    json.dump(label_dict, f, indent="\t")

def to_one_hot(labels, dimension=9):
    results = np.zeros((len(labels), dimension))
    for i, label in enumerate(labels):
        l = label_dict[label]
        results[i, l] = 1.
    return results

one_hot_train_y = to_one_hot(train_y)
one_hot_test_y = to_one_hot(test_y)

x_val = one_hot_train_x[:1000]
partial_x_train = one_hot_train_x[1000:]

y_val = one_hot_train_y[:1000]
partial_y_train = one_hot_train_y[1000:]

from keras import models, layers

model = models.Sequential()
model.add(layers.Dense(64, activation='relu', input_shape=(10000,)))
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(len(label_dict), activation='softmax'))

model.compile(optimizer='rmsprop',
             loss='categorical_crossentropy',
             metrics=['accuracy'])

history = model.fit(partial_x_train,
                   partial_y_train,
                   epochs=4,
                   batch_size=512,
                   validation_data=(x_val, y_val))

results = model.evaluate(one_hot_test_x, one_hot_test_y)
rating_result = {"loss": results[0],
                "accuracy": results[1],
                "train": len(train_x),
                "test": len(test_x)}

with open('output/rating_result.json', 'w', encoding='utf-8') as f:
    json.dump(rating_result, f, indent="\t")

model.save('output/rating_evaluate_model')

import pickle

with open('output/rating_tokenizer.pkl', 'wb') as f:
    pickle.dump(tokenizer, f)