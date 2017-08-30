from pymongo import MongoClient
from settings import MONGODB_HOST,MONGODB_PORT,MONGODB_DB,MONGODB_COLLECTION

class monve_db(object):
    def __init__(self, mongo_host= MONGODB_HOST, mongo_port= MONGODB_PORT,mongoDB = MONGODB_DB):
        self.mongo_host = mongo_host
        self.mongo_port = mongo_port
        self.mongo_db = mongoDB

    def DB_open(self):
        self.client = MongoClient(host = self.mongo_host,port= self.mongo_port)
        self.db = self.client[self.mongo_db]

    def update_item(self,item,collection = MONGODB_COLLECTION):

        self.db[collection].update({'title':item['title']},
                                             {'$set':item},True)

