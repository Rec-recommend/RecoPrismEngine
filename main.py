#!/usr/bin/env python3

from DbHandler.TenantDbHandler import TenantDbHandler
# from Recommenders.Surprise import CollborativeRecommender

import pandas as pd

# Helper functions #######################################


def prepare_df(table):
    df = pd.DataFrame(table['data'])
    df.columns = table['column_names']
    return df

# =====================================================


tenant = TenantDbHandler('test_eav')
items_table = tenant.get_eav_table('items')
df = prepare_df(items_table)

print(df.head())

# line_format = 'user item rating'
# sim_options = {'name': 'cosine', 'user_based': True, 'min_support': 20}

# cfr = CollborativeRecommender(df, line_format)
# cfr.set_sim_options(sim_options)
# cfr.calc_sim_matrix()

# print(cfr.get_similar_users(6539))

# import sys
# db_name = sys.argv[1]
# print(t.get_eav_table("items"))
