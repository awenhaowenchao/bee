"""
Common
"""
from bee.db.psd.criteria import CriteriaSet
from bee.db.psd.result import Result, Reader, ExecuteResult
from bee.db.psd.table import Table
from bee.db.psd.value import Value


class ResultClause():
    name = "ResultClause"

    def result(self) -> Result:
        pass


"""
insert clauses
"""


class InsertClause():
    name = "InsertClause"

    def columns(self, columns=[]):
        pass


class InsertResultClause():
    name = "InsertResultClause"

    def submit(self):
        pass

    def result(self):
        pass


class InsertValuesClause(InsertResultClause):
    name = "InsertValuesClause"

    def values(self, values=[]) -> "InsertValuesClause":
        pass


class InsertColumnsClause():
    name = "InsertColumnsClause"

    def values(self, values=[]) -> InsertValuesClause:
        pass


"""
update clauses
"""


class UpdateClause():
    """
    UpdateClause
    """
    name = "UpdateClause"

    def set(self, col: str, val):
        pass

    def inc(self, col: str, val):
        pass

    def dec(self, col: str, val):
        pass

    def expr(self, col: str, val):
        pass


class SetClause(UpdateClause, ResultClause):
    """
    SetClause
    """
    name = "SetClause"

    def where(self, CriteriaSet) -> ResultClause:
        pass


"""
delete clauses
"""


class DeleteClause():
    """
    DeleteClause
    """
    name = "DeleteClause"

    def where(self, CriteriaSet) -> ResultClause:
        pass


"""
Select clauses
"""


class SelectClause():
    """
    SelectClause
    """
    name = "SelectClause"

    def From(self, table: Table) -> "FromClause":
        pass


class LimitClause():
    """
    LimitClause
    """
    name = "LimitClause"

    def limit(self, skip: int, take: int) -> "SelectResultClause":
        pass

    def page(self, index: int, size: int) -> "SelectResultClause":
        pass


class SelectResultClause():
    """
    SelectResultClause
    """
    name = "SelectResultClause"

    def value(self) -> Value:
        pass

    def int(self) -> int:
        pass

    def scan(self, *dst):
        pass

    # def fill(self, i: object):
    #     pass
    def one(self, _type: type):
        pass

    def list(self, _type: type):
        pass

    def reader(self) -> Reader:
        pass

    def for_(self, fn: object):
        pass


class OrderByClause(LimitClause, SelectResultClause):
    pass


class GroupByClause(LimitClause, SelectResultClause):
    def order_by(self, *orders) -> "OrderByClause":
        pass

    def having(self, f: CriteriaSet) -> "HavingClause":
        pass


class HavingClause(LimitClause, SelectResultClause):
    def order_by(self, *orders) -> "OrderByClause":
        pass


class WhereClause(LimitClause, SelectResultClause):

    def group_by(self, *cols) -> GroupByClause:
        pass

    def order_by(self, *orders) -> "OrderByClause":
        pass


class FromClause(LimitClause, SelectResultClause):
    """
    FromClause
    """
    name = "FromClause"

    def Join(self, table: Table, on: CriteriaSet) -> "JoinClause":
        pass

    def left_join(self, t: Table, on: CriteriaSet) -> "JoinClause":
        pass

    def right_join(self, t: Table, on: CriteriaSet) -> "JoinClause":
        pass

    def full_join(self, t: Table, on: CriteriaSet) -> "JoinClause":
        pass

    def Where(self, f: CriteriaSet) -> WhereClause:
        pass

class JoinClause(FromClause):
    pass

"""
count clauses
"""


class CountResultClause():
    """
    CountResultClause
    """
    name = "CountResultClause"

    def value(self) -> int:
        pass

    def scan(self, dst):
        pass


class CountClause(CountResultClause):
    """
    CountClause
    """
    name = "CountClause"

    def join(self, table: Table, on: CriteriaSet) -> JoinClause:
        pass

    def left_join(self, t: Table, on: CriteriaSet) -> JoinClause:
        pass

    def right_join(self, t: Table, on: CriteriaSet) -> JoinClause:
        pass

    def full_join(self, t: Table, on: CriteriaSet) -> JoinClause:
        pass

    def where(self, f: CriteriaSet) -> WhereClause:
        pass


class CountGroupByClause():
    def having(self, f: CriteriaSet) -> CountResultClause:
        pass


class CountWhereClause(CountResultClause):

    def group_by(self, *cols) -> "CountGroupByClause":
        pass


"""
execute clauses
"""


class ExecuteClause():

    def result(self) -> ExecuteResult:
        pass

    def value(self) -> Value:
        pass

    def scan(self, *dst):
        pass

    def fill(self, i: object):
        pass

    def reader(self) -> Reader:
        pass

    def for_(self, fn: object):
        pass
