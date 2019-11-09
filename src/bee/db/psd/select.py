from enum import Enum
from typing import List

from bee.db.psd.clause import SelectClause, FromClause, WhereClause, JoinClause, GroupByClause, OrderByClause, HavingClause, \
    SelectResultClause
from bee.db.psd.column import new_expr_column, Columns
from bee.db.psd.criteria import CriteriaSet
from bee.db.psd.table import Table, to_table
from bee.db.psd.value import Value


class OrderEnum(Enum):
    ASC = 0,
    DESC = 1


class Join():
    name = "Join"

    def __init__(self, type: str, t: Table, on: CriteriaSet):
        self.type = type
        self.table = t
        self.on = on


class Order():
    name = "Order"

    def _init__(self, cols: Columns, t: OrderEnum):
        self.columns = cols
        self.type = t


class SelectInfo():
    name = "SelectInfo"

    def __init__(self, table: Table = None, distinct: bool = False, columns: Columns = None, where: CriteriaSet = None,
                 joins: List[Join] = None
                 , groups: object = None, having: CriteriaSet = None, orders: List[Order] = None, skip: int = 0,
                 take: int = 0,
                 count: bool = False):
        self.table = table
        self.distinct = distinct
        self.columns = columns
        self.where = where
        self.joins = []
        self.groups = groups
        self.having = having
        self.orders = orders
        self.skip = skip
        self.take = take,
        self.count = count


class SelectContext(SelectClause, FromClause, WhereClause):
    name = "SelectContext"

    def __init__(self, info: SelectInfo = None, db=None):
        self.info = info
        self.db = db

    def reset(self):
        self.info.distinct = False
        self.info.columns = None
        self.info.where = None
        self.info.joins = None
        self.info.groups = None
        self.info.having = None
        self.info.orders = None
        self.info.skip = 0
        self.info.take = 0
        self.info.count = False
        super().reset()

    def select(self, cols: Columns, *distinct: bool) -> SelectClause:
        self.info.columns = cols
        if distinct != None and len(distinct) > 0:
            self.info.distinct = distinct[0]
        return self

    def count(self, table: Table) -> FromClause:
        self.info.columns = [new_expr_column("COUNT(0)", "count")]
        self.info.table = to_table(table)
        return self

    def From(self, table: Table) -> FromClause:
        self.info.table = to_table(table)
        return self

    def Where(self, w: CriteriaSet) -> WhereClause:
        self.info.where = w
        return self

    def Join(self, t: Table, on: CriteriaSet) -> JoinClause:
        return self._join(t=t, on=on, jt="JOIN")

    def left_join(self, t: Table, on: CriteriaSet) -> JoinClause:
        return self._join(t, on, "LEFT JOIN")

    def right_join(self, t: Table, on: CriteriaSet) -> JoinClause:
        return self._join(t, on, "RIGHT JOIN")

    def full_join(self, t: Table, on: CriteriaSet) -> JoinClause:
        return self._join(t, on, "FULL JOIN")

    def _join(self, t: Table, on: CriteriaSet, jt: str) -> JoinClause:
        join = Join(type=jt, t=t, on=on)
        self.info.joins.append(join)
        return self

    def group_by(self, cols: Columns) -> GroupByClause:
        self.info.groups = cols
        return self

    def having(self, f: CriteriaSet) -> HavingClause:
        self.info.having = f
        return self

    def order_by(self, orders: Order) -> OrderByClause:
        self.info.orders = orders
        return self

    def limit(self, skip: int, take: int) -> SelectResultClause:
        self.info.skip = skip
        self.info.take = take
        return self

    def page(self, index: int, size: int) -> SelectResultClause:
        self.info.skip = (index - 1) * size
        self.info.take = size
        return self

    def value(self) -> Value:
        data = self.row().get("data")
        return data

    def int(self) -> int:
        data = self.row().get("data")
        if data != None and len(data) == 1:
            return data[0]
        else:
            return None

    def one(self, _type: type):
        row = self.row()
        if row == None:
            return None
        cols = row.get("cols")
        data = row.get("data")
        if data == None:
            return None
        ins = _type()
        for i in range(len(cols)):
            col = cols[i]
            # if hasattr(ins, col[0]):
            #     setattr(ins, col[0], data[i])
            setattr(ins, col[0], data[i])
        return ins

    def list(self, _type: type=None):

        rows = self.rows()
        if rows == None:
            return None
        cols = rows.get("cols")
        data_list = rows.get("data")

        if _type == None:
            return data_list

        ins_list = []
        if data_list == None or len(data_list) == 0:
            return []
        for data in data_list:
            ins = _type()
            for i in range(len(cols)):
                col = cols[i]
                # if hasattr(ins, col[0]):
                #     setattr(ins, col[0], data[i])
                setattr(ins, col[0], data[i])
            ins_list.append(ins)
        return ins_list

    def load(self):
        """
            orm
        :return:
        """
        pass

    def row(self):
        builder = self.db.p.build_select(info=self.info)
        return self.db.find_one(builder.value(), builder.args)

    def rows(self):
        builder = self.db.p.build_select(info=self.info)
        print(builder.value())
        return self.db.find_list(builder.value(), builder.args)
