from pymongo import MongoClient
import pprint
import pandas as pd
import json

with open("../letter-preprocess/secrets.json", 'r') as f:
    info = json.load(f)

mongo_host = "mongodb://{}:{}@{}:{}".format(info['mongo_info']['user'],
                                                    info['mongo_info']['password'],
                                                    info['host'],
                                                    info['mongo_info']['port'])
mongo = MongoClient(mongo_host)

db = mongo['rating_db']
posts = db.posts

df = pd.read_csv("../letter-rating-model/answer_rating.csv")

new_posts = []
for idx, row in df.iterrows():
    new_posts.append({"target": row['rating'],
                      "content": row['letter']})
results = posts.insert_many(new_posts)

print(posts.count_documents({}))

# print(db)
#
# for post in posts.find():
#     pprint.pprint(post)
#
# print(posts.count_documents({}))
