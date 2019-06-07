#!/usr/bin/env python3


class IAVQueryBuilder:

    def __init__(self, entity_name):
        self.entity_name = entity_name
        self.select_part = "Select iav1.id,"
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
        self.select_part += " iav"
        self.select_part += str(self.table_count)
        self.select_part += ".value as "
        self.select_part += attr_name
        self.select_part += ", "
        self.from_table()
        self.where(attr_name)
        return self

    def from_table(self):
        self.from_part += self.entity_name
        self.from_part += " as iav"
        self.from_part += str(self.table_count)
        self.from_part += ", "

    def where(self, attrname):
        self.where_part += " iav"
        self.where_part += str(self.table_count)
        self.where_part += ".attribute_id = "
        self.where_part += "(select id from attributes where label = '"
        self.where_part += attrname
        self.where_part += "') AND"

    def join(self):
        q = " "
        for i in range(1, self.table_count, 1):
            q += " iav" + str(i)
            q += ".item_id = iav" + str(i+1)
            q += ".item_id" + " AND "
        return q[:-4]

