#!/usr/bin/env python3

from DbHandler.TenantDbHandler import TenantDbHandler
from Recommenders.ContentBased import ContentBasedRecommender
import turicreate as tc
import pandas as pd
from pymongo import MongoClient
from turicreate import SFrame
import math
import sys


tenant_db_name = sys.argv[1]

# =====================================================
# store table in a dataframe
# -----------------------------------------------------
def prepare_df(table):
	try:
		df = pd.DataFrame(table['data'])
		df.columns = table['column_names']
	except:
		pass

	return df


# =====================================================
# load data from mysql and train the model
# -----------------------------------------------------
tenant_handler = TenantDbHandler(tenant_db_name)
df 	   		   = prepare_df(tenant_handler.get_pivot_table('ratings'))

if df.empty:
	exit()

train_data = tc.Sframe(df)

# =====================================================
# Content Based Algorithm Usage
# -----------------------------------------------------

# df = prepare_df(tenant_handler.get_iav_table())

# if df.empty:
# 	exit()

# features = []
# labels  = tenant_handler.get_iav_attributes('label')
# weights = tenant_handler.get_iav_attributes('weight')

# for (label, weight) in zip(labels, weights):
# 	features.append({"label": label, "weight": int(weight)})

# rec = ContentBasedRecommender(df, features)

# rec.calc_cosine_sim_matrix()

# res = rec.get_similar_items(72998)

m = tc.item_similarity_recommender.create(train_data, user_id='end_user_id', item_id='item_id', target='value',)

# =====================================================
# get users recommendations and store them in mongodb
# -----------------------------------------------------
mongo_client = MongoClient()
mongo_db = mongo_client['recoprism']
collection = tenant_db_name + "_users"

users = train_data['end_user_id'].unique()
mongo, count = [], 0
chuck_size = math.ceil(len(users)/10)
for user in users:
	recos = m.recommend(users=[user],k=20)
	mongo.append({'user_id':int(user), 'items':list(recos['item_id'])})
	count += 1
	if count % chuck_size == 0:
		mongo_db[collection].insert_many(mongo)
		mongo = []
