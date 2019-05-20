#!/usr/bin/env python3

from DbHandler import *

class TenantDbHandler:
    def __init__(self , DB_name):
        self.tenant_DbHandler = DbHandler()
        self.DB_name = DB_name
        self.db = self.tenant_DbHandler.connect_to_db(self.DB_name)

    def get_tables(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM configs where target = table")
        return cursor.fetchall()

    def get_columns(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM configs where target = column")
        return cursor.fetchall()

    def get_table_data(self , table_name):
        cursor = self.db.cursor()
        cursor.execute(f"SELECT * FROM {table_name} where target = column")
        return cursor.fetchall()


# DbHandler = TenantDbHandler('cart-on-rails')
# DbHandler.get_table_data('users')