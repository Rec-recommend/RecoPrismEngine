#!/usr/bin/env python3

from DbHandler import *
class SystemDbHandler:
    def __init__(self):
        self.system_DbHandler = DbHandler()
        self.db = self.system_DbHandler.connect_to_db("recoprism")

    def read_tenant_db_names(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM websites")
        return cursor.fetchall()


# DbHandler = SystemDbHandler()
# DbHandler.read_tenant_db_names()