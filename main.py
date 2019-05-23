#!/usr/bin/env python3

from DbHandler.SystemDbHandler import SystemDbHandler
from DbHandler.TenantDbHandler import TenantDbHandler
from Recommenders.Surprise import CollborativeRecommender

import pandas as pd

# import sys
# db_name = sys.argv[1]

system_db_handler = SystemDbHandler()
tenant_db_name = system_db_handler.read_tenant_db_names()[0]

tenant_db_handler = TenantDbHandler(tenant_db_name)

for table_name in tenant_db_handler.get_tables():
    tenant_table = tenant_db_handler.get_table_data(table_name)
    df = pd.DataFrame(tenant_table['data'])
    df.columns = tenant_table['column_names']
    df = df.drop(['created_at', 'updated_at', 'id'], axis=1)

    line_format = 'user item rating'
    sim_options = {'name': 'pearson_baseline', 'user_based': True}

    cfr = CollborativeRecommender(df, line_format)
    cfr.set_sim_options(sim_options)
    cfr.calc_sim_matrix()

    print(cfr.get_similar_users(2))