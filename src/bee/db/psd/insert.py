from typing import List

from bee.db.psd.clause import InsertClause, InsertColumnsClause, InsertValuesClause, InsertResultClause
from bee.db.psd.column import ColumnFilter
from bee.db.psd.orm import Model


class InsertInfo():
    name = "InsertInfo"

    def __init__(self, table, filter: ColumnFilter=None):
        self.table = table
        self.columns = ()
        self.values = []
        self.filter = filter


class InsertContext(InsertClause, InsertColumnsClause, InsertValuesClause, InsertResultClause):
    name = "InsertContext"

    def __init__(self, info=None, db=None):
        self.info = info
        self.db = db

    def reset(self):
        self.info.columns = None
        self.info.values = None
        self.info.filter = None
        super().reset();
        # super(InsertContext, self).result(); python2.7

    def insert(self, table) -> InsertClause:
        self.info.table = table
        return self

    def save(self, i: Model, *filters: ColumnFilter):
        """
        orm
        :return:
        """
        if len(filters) > 0:
            self.info.filter = filters[0]
        if i != None:
            self.info.table = i.getValue("__table__")

        if self.info.filter == None:
            """
            没有字段filter
            """
            self.info.columns = list(i.keys())
            self.info.values = [list(i.values())]
            self.submit()
        else:
            #TODO:
            pass

    def save_list(self, i: List[Model], *filters: ColumnFilter):
        pass

    def columns(self, *columns: str) -> InsertColumnsClause:
        self.info.columns = columns
        return self

    def values(self, *values) -> InsertValuesClause:
        # print(id(self.info))
        # print(id(self.info.values))
        if self.info.values != None:
            # self.info.values += values
            self.info.values.append(values)
        else:
            self.info.values = list(values)
        return self

    def submit(self):
        return self.result()

    def result(self):
        builder = self.db.p.build_insert(info=self.info)

        return self.db.conn.exec(builder.value(), builder.args)
