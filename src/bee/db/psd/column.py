from typing import List

from bee.db.psd.table import Table, to_table


class ColumnFilter():
    def filter(self, cols: List[str]) -> List[str]:
        pass


class Column():

    def __init__(self, name: str):
        pass

    def table(self) -> Table:
        pass

    def name(self) -> str:
        pass

    def alias(self) -> str:
        pass

    def field(self) -> str:
        pass


class Columns(List[Column]):
    def __init__(self, *items):
        if len(items) == 0:
            super().__init__([])
        else:
            super().__init__(items)

    @staticmethod
    def new_columns(*cols: str) -> "Columns":
        columns = Columns([])
        for c in cols:
            columns.append(SimpleColumn[SimpleColumn])
        return columns
    def simple(self, *cols: str) -> "Columns":
        columns = Columns()
        for col in cols:
            columns.append(SimpleColumn(col))
        return columns

    def get_table(self, t, *cols: str) -> "Columns":
        columns = Columns()
        for col in cols:
            columns.append(TableColumn(t=to_table(t),name=col))
        return columns

    def get_alias(self, t, col: str, alias: str) -> "Columns":
        columns = Columns()
        columns.append(TableColumn(t=to_table(t),name=col, alias=alias))
        return columns

    def get_expr(self, expr: str, alias: str) -> "Columns":
        columns = Columns()
        columns.append(ExprColumn(expr=expr, alias=alias))
        return columns

def new_columns(*cols: str) -> Columns:
    columns = Columns()
    for col in cols:
        # columns.append(SimpleColumn(col))
        if isinstance(col, str):
            columns.append(SimpleColumn(col))
        else:
            # TODO; complex logic, it's wrong
            columns.append(col)
    return columns


class SimpleColumn(str):

    def __init__(self, name: str):
        self._name = name
        super().__init__()

    def table(self) -> Table:
        return None

    def name(self) -> str:
        return self._name

    def alias(self) -> str:
        return ""

    def field(self) -> str:
        return self._name


def new_column(name: str, alias: str):
    if alias == None:
        SimpleColumn(name)
    else:
        new_table_column(name, alias)


class TableColumn(Column):
    name = "TableColumn"

    def __init__(self, t: Table, name: str, alias: str):
        self._table = t
        self._name = name
        self._alias = alias
        super.__init__()

    @staticmethod
    def new_table_column(t: Table, name: str, alias: str):
        tc = Table(t, name)
        if alias != None and alias != "":
            tc.alias = alias

        return tc

    def table(self) -> Table:
        return self._table

    def name(self) -> str:
        return self._name

    def alias(self) -> str:
        return self._alias

    def field(self) -> str:
        if self.alias == None or self.alias == "":
            return self.name
        else:
            return self.alias



def new_table_column(t: Table, name: str, alias: str):
    tc = Table(t, name)
    if alias != None and alias != "":
        tc.alias = alias

    return tc


class ExprColumn(Column):
    name = "ExprColumn"

    @staticmethod
    def new_expr_column(expr: str, alias: str) -> "ExprColumn":
        return ExprColumn(expr, alias)

    def __init__(self, expr: str, alias: str):
        self._expr = expr
        self._alias = alias
        super().__init__(expr)

    def table(self) -> Table:
        return None

    def name(self) -> str:
        return self._expr

    def expr(self) -> str:
        return self._expr

    def alias(self) -> str:
        return self._alias

    def field(self) -> str:
        return self._alias


def new_expr_column(expr: str, alias: str) -> ExprColumn:
    return ExprColumn(expr, alias)
