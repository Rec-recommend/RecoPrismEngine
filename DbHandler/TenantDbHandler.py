#!/usr/bin/env python3

from DbHandler.DbHandler import DbHandler
from DbHandler.IAVQueryBuilder import IAVQueryBuilder


class TenantDbHandler:

    def __init__(self, db_name):
        self.tenant_DbHandler = DbHandler()
        self.db_name = db_name
        self.db = self.tenant_DbHandler.connect_to_db(self.db_name)

    def get_iav_attributes(self, column):
        q = "SELECT " + column + " FROM attributes "
        cursor = self.db.cursor()
        cursor.execute(q)
        weights = cursor.fetchall()
        x = []
        for item in weights:
            x.extend(item)
        return x

    def get_iav_table(self):
        labels = self.get_iav_attributes("label")
        weights = self.get_iav_attributes("weight")
        qb = IAVQueryBuilder('iav')
        for label in labels:
            qb.attribute(label)
        q = qb.build()
        cursor = self.db.cursor()
        cursor.execute(q)

        data = cursor.fetchall()
        labels.insert(0, 'item_id')
        weights.insert(0, 0)
        return {
            "column_names": labels,
            "weights": weights,
            "data": data
        }

    def get_pivot_table(self, pivot_table_name):
        cursor = self.db.cursor()
        cursor.execute('select end_user_id, item_id, value from ' + pivot_table_name)
        data = cursor.fetchall()
        return {
            "column_names": cursor.column_names,
            "data": data
        }
