#!/usr/bin/env python3

from dotenv import dotenv_values
import mysql.connector

# Load enviroment variables
env = dotenv_values()

class DbHandler:

    def connect_to_db(self,db_name):
        db = mysql.connector.connect(
                host = env['host'],
                user = env['user'],
                password = env['password'],
                database = db_name
        )
        return db






# db1 = DbHandler.connect_to_db("cart-on-rails")
# db2 = DbHandler.connect_to_db("ruby_users_api")


# cursor1 = db1.cursor()
# cursor2 = db2.cursor()

# cursor1.execute("SELECT * FROM users")
# cursor2.execute("SELECT * FROM users")
# print(cursor1.fetchall())
# print(cursor2.fetchall())
