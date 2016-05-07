from pymongo import MongoClient
from bson import ObjectId


def mongo_connect(db, collection):
    client = MongoClient('localhost', 27017)
    db = client[db]
    collection = db[collection]
    return client, db, collection


def check_id(id, collection):
    if collection.find({"_id": id}).count() == 1:
        return False
    else:
        return True
