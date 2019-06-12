
from DbHandler.SystemDbHandler import SystemDbHandler
import os

system_handler = SystemDbHandler()
tenants_dbs = system_handler.get_tenant_db_names()

for db in tenants_dbs:
    command = "python3 main.py " + db
    os.system(command)