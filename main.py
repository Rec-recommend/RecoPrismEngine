#!/usr/bin/env python3

from DbHandler.TenantDbHandler import TenantDbHandler
from DbHandler.MongoHandler import MongoHandler
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
mongo_handler  = MongoHandler(tenant_db_name)
tenant_handler = TenantDbHandler(tenant_db_name)
df 	   		   = prepare_df(tenant_handler.get_pivot_table('ratings'))

if df.empty:
	exit()

train_data = tc.SFrame(df)


# m = tc.item_similarity_recommender.create(train_data, user_id='end_user_id', item_id='item_id', target='value',)

# =====================================================
# get users recommendations and store them in mongodb
# -----------------------------------------------------

# users = train_data['end_user_id'].unique()

# mongo_handler.insert_chunk("users",users,m)

# =====================================================
# Content Based Algorithm Usage
# -----------------------------------------------------

df = prepare_df(tenant_handler.get_iav_table())
if df.empty:
	exit()

features = []
labels   = tenant_handler.get_iav_attributes('label')
weights  = tenant_handler.get_iav_attributes('weight')

for (label, weight) in zip(labels, weights):
	features.append({"label": label, "weight": int(weight)})

rec = ContentBasedRecommender(df, features)

rec.calc_cosine_sim_matrix()

# =====================================================
# get items recommendations and store them in mongodb
# -----------------------------------------------------

items = train_data['item_id'].unique()

mongo_handler.insert_chunk("items",items,rec)
