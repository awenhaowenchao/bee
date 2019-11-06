from bee.db.psd.column import new_columns, ColumnFilter, Columns
from bee.db.psd.criteria import SimpleCriteriaSet, CriteriaSet, not_, and_, or_, equal
from bee.db.psd.select import Order, OrderEnum
from bee.db.psd.table import Table, new_table


def ASC(cols: str) -> Order:
    return Order(cols=C(cols), t=OrderEnum.ASC)


def DESC(*cols: str) -> Order:
    return Order(cols=C(cols), t=OrderEnum.DESC)


def T(name: str, *alias: str) -> Table:
    return new_table(name, *alias)


def C(*cols: str)  -> Columns:
    return new_columns(*cols)


def CT(t, *cols: str):
    return new_columns().get_table(t, *cols)


def CX(expr: str, alias: str=None):
    return new_columns().get_expr(expr, alias)


def Omit(*cols: str) -> ColumnFilter:
    # TODO: omit-filter
    pass


def Include(*cols: str) -> ColumnFilter:
    # TODO: include-filter
    pass


def W() -> SimpleCriteriaSet:
    return SimpleCriteriaSet()


def Not(inner: CriteriaSet) -> CriteriaSet:
    return not_(inner)


def And(left: CriteriaSet, right: CriteriaSet) -> CriteriaSet:
    return and_(left, right)


def Or(left: CriteriaSet, right: CriteriaSet) -> CriteriaSet:
    return or_(left, right)


def Equal(col, val) -> SimpleCriteriaSet:
    return equal(col, val)


def On(left, right) -> SimpleCriteriaSet:
    return W().equal2(left, right)
