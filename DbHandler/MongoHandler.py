from pymongo import MongoClient
import math

class MongoHandler():
    def __init__(self,tenant_db_name):
        mongo_client        = MongoClient()
        self.mongo_db       = mongo_client['recoprism']
        self.tenant_db_name = tenant_db_name

    def insert_chunk(self,model,entities,reco):
        collection = self.tenant_db_name + "_" + model
        mongo, count = [], 0
        chuck_size = math.ceil(len(entities)/10)
        for entity in entities:
            if model == "users" :
                recos = reco.recommend(users=[entity],k=20)
                mongo.append({'user_id':int(entity), 'items':list(recos['item_id'])})
            else:
                recos = reco.get_similar_items(entity)[1:20]
                mongo.append({'item_id':int(entity), 'items':list(recos)})
            count += 1
            if count % chuck_size == 0:
                self.mongo_db[collection].insert_many(mongo)
                mongo = []