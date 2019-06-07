#!/usr/bin/env python3

from DbHandler.TenantDbHandler import TenantDbHandler
from Recommenders.CollborativeRecommender import CollborativeRecommender
import pandas as pd

# Helper functions #######################################

# dict for movies names and ids
# --------------------------------
movies_df = pd.read_csv('./Recommenders/movies.csv')
movieID_to_name = {}

for index, row in movies_df.iterrows():
	movieID = int(row[0])
	movieName = row[1]
	movieID_to_name[movieID] = movieName


# store table in a dataframe
# --------------------------------
def prepare_df(table):
    df = pd.DataFrame(table['data'])
    df.columns = table['column_names']
    return df

# =====================================================


tenant = TenantDbHandler('tn_GfxfFrKRovHKGJ4PNr4lOArxQNQEb')
items_table = tenant.get_pivot_table('ratings')
df = prepare_df(items_table)
print(df.head(20))


line_format = 'user item rating'
sim_options = {'name': 'pearson_baseline', 'user_based': True, 'min_support': 5}

cfr = CollborativeRecommender(sim_options, df, line_format)


movies = ['2']

for movie in movies:
	res = cfr.get_recommendations(movie)
	for movie in res:
		print(movieID_to_name[movie[0]] , " ---- " , movie[1])
	print("--------------------------------------")









# import sys
# db_name = sys.argv[1]
# print(t.get_eav_table("items"))
# file_path = "./Recommenders/ratings.1.csv"
# cfr = CollborativeRecommender(sim_options, file_path, line_format)