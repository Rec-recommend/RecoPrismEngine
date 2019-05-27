#!/usr/bin/env python3

from DbHandler.DbHandler import DbHandler
from DbHandler.EAVQueryBuilder import EAVQueryBuilder


class TenantDbHandler:

    def __init__(self, db_name):
        self.tenant_DbHandler = DbHandler()
        self.db_name = db_name
        self.db = self.tenant_DbHandler.connect_to_db(self.db_name)

    def get_eav_attributes(self, column,entity_name):
        q = "SELECT " + column + " FROM attributes \
        where entity_id = (select id from entities where name ='" + entity_name + "')"
        cursor = self.db.cursor()
        cursor.execute(q)
        weights = cursor.fetchall()
        x = []
        for item in weights:
            x.extend(item)
        return x

    def get_eav_table(self, entity_name):
        labels = self.get_eav_attributes("label", entity_name)
        weights = self.get_eav_attributes("weight", entity_name)
        qb = EAVQueryBuilder(entity_name)
        for label in labels:
            qb.attribute(label)
        q = qb.build()
        cursor = self.db.cursor()
        print(q)
        cursor.execute(q)

        data = cursor.fetchall()
        labels.insert(0, 'id')
        weights.insert(0, 0)
        return {
            "column_names": labels,
            "weights": weights,
            "data": data
        }

    def get_pivot_table(self, pivot_table):
        cursor = self.db.cursor()
        cursor.execute('select user_id, item_id, value from ' + pivot_table)
        data = cursor.fetchall()
        return {
            "column_names": cursor.column_names,
            "data": data
        }
