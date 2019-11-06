from bee.db.psd.clause import UpdateClause, SetClause, ResultClause
from bee.db.psd.column import ColumnFilter
from bee.db.psd.criteria import CriteriaSet, SimpleCriteriaSet
from bee.db.psd.orm import Model


class UpdateInfo():
    name = "UpdateInfo"

    def __init__(self, table, where: CriteriaSet = None, filter=None):
        self.table = table
        self.columns = []
        self.values = []
        self.where = where
        self.filter = filter


class UpdateContext(SetClause, UpdateClause, ResultClause):
    name = "UpdateContext"

    def __init__(self, info: UpdateInfo = None, db=None):
        self.info = info
        self.db = db

    def reset(self):
        self.info.columns = None
        self.info.values = None
        self.info.filter = None
        super().reset();

    def update(self, table) -> UpdateClause:
        self.info.table = table
        return self

    def modify(self, i: Model, *filters: ColumnFilter):
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
            self.info.values = list(i.values())
        else:
            # TODO:
            pass

        # Where
        pk = i.getValue("__primary_key__")
        where = SimpleCriteriaSet()
        where.equal(pk, i.getValue(pk))
        self.info.where = where
        return self.result()



    def set(self, col: str, val) -> SetClause:
        """
        set statement
        :param col:
        :param val:
        :return:
        """
        self.info.columns.append(col)
        self.info.values.append(val)
        return self

    def inc(self, col: str, val: object) -> SetClause:
        pass

    def dec(self, col: str, val: object) -> SetClause:
        pass

    def expr(self, col: str, val: object) -> SetClause:
        pass

    def where(self, where: CriteriaSet) -> ResultClause:
        self.info.where = where
        return self

    def result(self):
        builder = self.db.p.build_update(info=self.info)
        return self.db.conn.exec(builder.value(), builder.args)
