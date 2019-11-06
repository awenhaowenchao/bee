from bee.db.psd.clause import DeleteClause, ResultClause
from bee.db.psd.criteria import CriteriaSet, SimpleCriteriaSet
from bee.db.psd.orm import Model


class DeleteInfo():
    name = "DeleteInfo"

    def __init__(self, table: str, where: CriteriaSet = None):
        self.table = table
        self.where = where


class DeleteContext(DeleteClause, ResultClause):
    name = "DeleteContext"

    def __init__(self, info: DeleteInfo = None, db=None):
        self.info = info
        self.db = db

    def reset(self):
        self.info.table = None
        self.info.where = None
        super().reset();

    def delete(self, table) -> DeleteClause:
        self.info.table = table
        return self

    def remove(self, i: Model):
        """
        orm
        :return:
        """

        if i != None:
            self.info.table = i.getValue("__table__")

        self.info.columns = list(i.keys())
        self.info.values = list(i.values())

        # Where
        pk = i.getValue("__primary_key__")
        where = SimpleCriteriaSet()
        where.equal(pk, i.getValue(pk))
        self.info.where = where
        return self.result()

    def where(self, where: CriteriaSet) -> ResultClause:
        self.info.where = where
        return self

    def result(self):
        builder = self.db.p.build_delete(info=self.info)
        return self.db.conn.exec(builder.value(), builder.args)
