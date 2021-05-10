from pyspark import SparkContext, SparkConf
from pymongo import MongoClient
from gb_preprocess import GBProcessor
from rating_preprocess import RatingPreprocessor
import sys
import json
import subprocess

if __name__ == '__main__':
    with open("secrets.json", 'r') as f:
        info = json.load(f)

    master = "spark://{}:{}".format(info['host'], info['spark_info']['port'])

    conf = SparkConf().setAppName("preprocessor").setMaster(master)
    sc = SparkContext(conf=conf)

    files = sc.wholeTextFiles("hdfs:///datafiles/jk")

    # no file in hdfs
    cnt = files.count()
    if cnt == 0:
        sys.exit(0)

    file_list = files.collect()

    for file in file_list:
        filePath = file[0]
        text = file[1]

        gbp = GBPreprocessor(text)
        good, bad = gbp.extract_gb()

        rp = RatingPreprocessor(file)
        result = rp.extract_rating()

        # save to mongo db
        mongo_host = "mongodb://{}:{}@{}:{}".format(info['mongo_info']['user'],
                                                    info['mongo_info']['password'],
                                                    info['host'],
                                                    info['mongo_info']['port'])
        mongo = MongoClient(mongo_host)

        if (good is not None) or (bad is not None):
            gb_db = mongo['letter_db']
            posts = gb_db.posts
            posts.insert_many(good.extend(bad))

        if result is not None:
            rating_db = mongo['rating_db']
            posts = rating_db.posts
            posts.insert_one(result)

        # remove file from hdfs
        subprocess.call(["hdfs", "dfs", "-rm", filePath])

