from bee.data import const
from bee.db.psd.builder import Builder
from bee.db.psd.column import SimpleColumn, ExprColumn, Column
from bee.db.psd.criteria import CriteriaSet, SimpleCriteriaSet, OneColumnCriteria, TwoColumnCriteria, ExprCriteria, \
    NotCriteriaSet, JoinCriteriaSet, CriteriaEnum
from bee.db.psd.delete import DeleteInfo
from bee.db.psd.insert import InsertInfo
from bee.db.psd.select import SelectInfo
from bee.db.psd.table import AliasTable
from bee.db.psd.update import UpdateInfo
from bee.errors.error import BeeError

const.psd_provider_comma = ','
const.psd_provider_dot = '.'

insertValueClauses = (
    "(?)",
    "(?,?)",
    "(?,?,?)",
    "(?,?,?,?)",
    "(?,?,?,?,?)",
    "(?,?,?,?,?,?)",
    "(?,?,?,?,?,?,?)",
    "(?,?,?,?,?,?,?,?)",
    "(?,?,?,?,?,?,?,?,?)",
    "(?,?,?,?,?,?,?,?,?,?)",  # 10
    "(?,?,?,?,?,?,?,?,?,?,?)",
    "(?,?,?,?,?,?,?,?,?,?,?,?)",
    "(?,?,?,?,?,?,?,?,?,?,?,?,?)",
    "(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
    "(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
    "(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
    "(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
    "(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
    "(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
    "(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",  # 20
)

class BuildError(BeeError):
    pass

class IProvider():
    name = "psd.provider.IProvider"

    def build_insert(self, info):
        pass

    def build_delete(self, info):
        pass

    def build_update(self, info):
        pass

    def build_select(self, info):
        pass

    def build_call(self, info):
        pass


class Provider(IProvider):

    def quote(self, builder, string):
        # builder.Query += string
        builder.write(string)
        pass

    def limit(self, builder, skip, take):
        pass

    def call(self, builder, sp, args=[]):
        pass

    def build_insert(self, info: InsertInfo = None) -> Builder:
        builder = Builder()

        cols = info.columns.__len__()
        builder.write("INSERT INTO ")
        self.quote(builder, info.table)
        builder.write("(" + info.columns[0])
        for i in range(cols):
            if i > 0:
                builder.write(const.psd_provider_comma)
                self.quote(builder, info.columns[i])
        builder.write(") VALUES ")
        rows = info.values.__len__()
        for i in range(rows):
            if i > 0:
                builder.write(const.psd_provider_comma)
            if i > 20:
                builder.write("( ?")
                for j in range(cols):
                    builder.write(", ?")
                builder.write(")")
            else:
                builder.write(insertValueClauses[cols - 1])
        builder.args = []
        for v in info.values:
            builder.args += v
        # builder.args += v
        return builder

    def build_update(self, info: UpdateInfo = None) -> Builder:

        builder = Builder()
        builder.write("UPDATE ")
        self.quote(builder, info.table)
        builder.write(" SET ")

        cols = info.columns.__len__()
        for i in range(cols):
            if i > 0:
                builder.write(const.psd_provider_comma)
            self.quote(builder, info.columns[i])
            builder.write("=")
            builder.write("?")
        builder.args = info.values
        if hasattr(info, "Where") and info.where != None:
            builder.write(" WHERE ")
            self.build_criteria_set(builder, info.where)
        return builder

    def build_delete(self, info: DeleteInfo = None):

        builder = Builder()
        builder.write("DELETE FROM ")
        self.quote(builder, info.table)

        if not hasattr(info, "Where") or info.where == None:
            raise BuildError("delete action must have Where clause")

        builder.write(" WHERE ")
        self.build_criteria_set(builder, info.where)

        return builder

    def build_select(self, info: SelectInfo = None):
        builder = Builder()
        builder.write("SELECT ")
        if info.distinct != None and info.distinct == True:
            builder.write("DISTINCT ")

        for i, col in enumerate(info.columns):
            if i > 0:
                builder.write(",")
            if col.table() == None:
                if isinstance(col, SimpleColumn):
                    builder.write(col)
                elif isinstance(col, ExprColumn):
                    builder.write(col.expr())
                else:
                    builder.write(col.name())
            else:
                self.quote(builder, col.table().prefix())
                builder.write(const.psd_provider_dot)
                self.quote(builder, col.name())

            if col.alias() !=None and col.alias() != "":
                builder.write_strs(" AS ", col.alias())

        builder.write(" FROM ")
        if isinstance(info.table, AliasTable):
            self.quote(builder, info.table.name())
        else:
            self.quote(builder, info.table)

        if info.table.alias() != None and info.table.alias() != "":
            builder.write_strs(" AS ", info.table.alias())

        self.build_join(builder, info)

        if info.where != None and not info.where.empty():
            builder.write(" WHERE ")
            self.build_criteria_set(builder, info.where)

        self.build_group_by(builder, info)
        return builder

    def build_criteria_set(self, builder, cs: CriteriaSet):
        if isinstance(cs, SimpleCriteriaSet):
            for index, value in enumerate(cs.items):
                if index > 0:
                    builder.write(" AND ")
                if isinstance(value, OneColumnCriteria):
                    self.build_one_column_criteria(builder, value)
                elif isinstance(value, TwoColumnCriteria):
                    self.build_two_column_criteria(builder, value)
                elif isinstance(value, ExprCriteria):
                    builder.write(str(value))

        elif isinstance(cs, NotCriteriaSet):
            builder.write(" NOT")
            self.build_criteria_set(builder, cs.inner)
            builder.write(")")
        elif isinstance(cs, JoinCriteriaSet):
            if (cs.left().empty()):
                self.build_criteria_set(builder, cs.rght())
            elif cs.rght().empty():
                self.build_criteria_set(builder, cs.left())
            else:
                builder.write("(")
                self.build_criteria_set(builder, cs.left())
                builder.write_strs(") ", cs.joiner(), " (")
                self.build_criteria_set(builder, cs.rght())
                builder.write(")")

    def build_one_column_criteria(self, builder, c: OneColumnCriteria):
        if c.table() != None:
            self.quote(builder, c.table().prefix())
            builder.write(const.psd_provider_dot)

        if c.type == CriteriaEnum.NE:
            if c.value == None:
                self.quote(builder, c.col)
                builder.write(" IS NOT NULL")
                return
            self.quote(builder, c.col)
            builder.write("<>?")
        elif c.type == CriteriaEnum.LT:
            self.quote(builder, c.col)
            builder.write("<?")
        elif c.type == CriteriaEnum.LTE:
            self.quote(builder, c.col)
            builder.write("<=?")
        elif c.type == CriteriaEnum.GT:
            self.quote(builder, c.col)
            builder.write(">?")
        elif c.type == CriteriaEnum.GTE:
            self.quote(builder, c.col)
            builder.write(">=?")
        elif c.type == CriteriaEnum.IN:
            self.quote(builder, c.col)
            builder.write(" IN(")
            self.build_in_values(builder, c.value)
            builder.write(")")
        elif c.type == CriteriaEnum.NIN:
            self.quote(builder, c.col)
            builder.write(" NOT IN(")
            self.build_in_values(builder, c.value)
            builder.write(")")
        elif c.type == CriteriaEnum.LK:
            self.quote(builder, c.col)
            builder.write_strs(" LIKE '", c.value, "'")
        else:
            if c.value == None:
                self.quote(builder, c.col)
                builder.write(" IS NOT NULL")
            self.quote(builder, c.col)
            builder.write("=?")
        if (isinstance(c.value, list)):
            builder.args += c.value
        else:
            builder.args.append(c.value)

    def build_in_values(self, builder, val):
        if isinstance(val, list):
            for index, value in enumerate(val):
                if index > 0:
                    builder.write(",")
                # if (isinstance(value, str)):
                #     builder.write_strs("'", value, "'")
                # else:
                #     builder.write(str(value))
                if (isinstance(value, str)):
                    builder.write_strs("'?'")
                else:
                    builder.write("?")


    def build_two_column_criteria(self, builder, c: TwoColumnCriteria):
        if not isinstance(c.left, str) and c.left.table() != None:
            self.quote(builder, c.left.table().prefix())
            builder.write(const.psd_provider_dot)

        if not isinstance(c.left, str):
            self.quote(builder, c.left.name())
        else:
            self.quote(builder, c.left)


        if c.type == CriteriaEnum.EQ:
            builder.write("=")
        elif c.type == CriteriaEnum.NE:
            builder.write("<>")
        elif c.type == CriteriaEnum.LT:
            builder.write("<")
        elif c.type == CriteriaEnum.LTE:
            builder.write("<=")
        elif c.type == CriteriaEnum.GT:
            builder.write(">")
        elif c.type == CriteriaEnum.GTE:
            builder.write(">=")
        else:
            # 默认使用等于
            builder.write("=")

        if hasattr(c.right, "table") and c.right.table() != None:
            self.quote(builder, c.right.table().prefix())
            builder.write(const.psd_provider_dot)
        if isinstance(c.right, str):
            self.quote(builder, c.right)
        else:
            self.quote(builder, c.right.name())

    def build_join(self, builder, info: SelectInfo):
        if info.joins != None and len(info.joins) > 0:
            for i, v in enumerate(info.joins):
                builder.write_strs(" ", v.type, " ")

                if isinstance(v.table, AliasTable):
                    self.quote(builder, v.table.name())
                else:
                    self.quote(builder, v.table)

                if not isinstance(v.table, str):
                    if v.table.alias() != None and v.table.alias() != "":
                        builder.write_strs(" AS ", v.table.alias())
                builder.write(" ON ")
                self.build_criteria_set(builder, v.on)

    def build_group_by(self, builder, info: SelectInfo):
        if info.groups != None and len(info.groups) > 0:
            builder.write(" GROUP BY ")
            for i, col in enumerate(info.groups):
                if i > 0:
                    builder.write(const.psd_provider_comma)
                    self.build_column(builder, col)
            if info.having != None:
                builder.write(" HAVING ")
                self.build_criteria_set(builder, info.having)

    def build_column(self, builder, col: Column):
        if col.table() == None and col.table() == "":
            self.quote(builder, col.name())
        else:
            self.quote(builder, col.table().prefix())
            builder.write(const.psd_provider_dot)
            self.quote(builder, col.name())
