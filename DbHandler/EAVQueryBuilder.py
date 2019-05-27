#!/usr/bin/env python3


class EAVQueryBuilder:

    def __init__(self, entity_name):
        self.entity_name = entity_name
        self.select_part = "Select eav1.id,"
        self.from_part = " FROM "
        self.where_part = " WHERE "
        self.table_count = 0

    def build(self):
        q = self.select_part[:-2]
        q += self.from_part[:-2]
        q += self.where_part
        q += self.join()
        return q

    def attribute(self, attr_name):
        self.table_count += 1
        self.select_part += " eav"
        self.select_part += str(self.table_count)
        self.select_part += ".value as "
        self.select_part += attr_name
        self.select_part += ", "
        self.from_table()
        self.where(attr_name)
        return self

    def from_table(self):
        self.from_part += self.entity_name
        self.from_part += " as eav"
        self.from_part += str(self.table_count)
        self.from_part += ", "

    def where(self, attrname):
        self.where_part += " eav"
        self.where_part += str(self.table_count)
        self.where_part += ".attr_id = "
        self.where_part += "(select id from attributes where label = '"
        self.where_part += attrname
        self.where_part += "')"

    def join(self):
        q = " AND "
        for i in range(1, self.table_count, 1):
            q += " eav" + str(i)
            q += ".id = eav" + str(i+1)
            q += ".id" + " AND "
        return q[:-4]

