#!/usr/bin/env python3

from DbHandler.DbHandler import DbHandler

class SystemDbHandler:
    def __init__(self):
        self.system_DbHandler = DbHandler()
        self.db = self.system_DbHandler.connect_to_db("recoprism")

    def read_tenant_db_names(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT uuid FROM websites")
        return [item[0] for item in cursor.fetchall()]


# DbHandler = SystemDbHandler()
# print(DbHandler.read_tenant_db_names())