#!/usr/bin/env python3

from DbHandler.DbHandler import DbHandler

class TenantDbHandler:
    def __init__(self , DB_name):
        self.tenant_DbHandler = DbHandler()
        self.DB_name = DB_name
        self.db = self.tenant_DbHandler.connect_to_db(self.DB_name)

    def get_tables(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT name FROM configs where target = 'table'")
        return [item[0] for item in cursor.fetchall()]

    def get_columns(self,table_name):
        cursor = self.db.cursor()
        cursor.execute(f"SELECT name , weight  FROM configs where target = 'column' and  `table` = '{table_name}' and used = 1")
        return cursor.fetchall()

    def get_table_data(self , table_name):
        cursor = self.db.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        return {
            "column_names": cursor.column_names,
            "data": cursor.fetchall()
            }



# DbHandler = TenantDbHandler('cart-on-rails')
# DbHandler.get_table_data('users')