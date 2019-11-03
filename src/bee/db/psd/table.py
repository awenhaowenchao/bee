class Table():
    def name(self) -> str:
        pass

    def alias(self) -> str:
        pass

    def prefix(self) -> str:
        pass


def to_table(table: object) -> "Table":
    if isinstance(table, str):
        return SimpleTable(table)
    elif isinstance(table, Table):
        return table


def new_table(name: str, *alias) -> "Table":
    if len(alias) == 0:
        return SimpleTable(name)
    else:
        return new_alias_table(name, alias[0])


class SimpleTable(str, Table):

    def __init__(self, t: str):
        self.t = t

    def name(self) -> str:
        return self.t

    def alias(self) -> str:
        return ""

    def prefix(self) -> str:
        return self.t


class AliasTable(Table):

    def __init__(self, name: str, alias: str, prefix: str):
        self._name = name
        self._alias = alias
        self._prefix = prefix

    def name(self) -> str:
        return self._name

    def alias(self) -> str:
        return self._alias

    def prefix(self) -> str:
        return self._prefix


def new_alias_table(name, alias):
    prefix = ""
    if alias == "":
        prefix = name
    else:
        prefix = alias
    return AliasTable(name, alias, prefix=prefix)
