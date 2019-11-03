from datetime import datetime

from bee import Psd, CX
from bee import Model, IntegerField, StringField, DateTimeField, Equal, W, C
from bee.errors.error import BeeError

db_test = Psd.open("test")
# 1)
with db_test.connection() as conn:
    db_test.insert("test").columns("id", "name", "remark").values(8, "james8", "remark8").result()

# 2)
with db_test.connection() as conn:
    db_test.insert("test").columns("id", "name").values(9, "james9").values(10, "james10").values(11, "james11").result()


# 3)
with db_test.connection() as conn:
    db_test.update("test").set("remark", "11111").where(Equal("id", "1")).result()

# 4)
with db_test.transaction():
    db_test.insert("test").columns("id", "name").values(18, "james18").result()
    raise BeeError("rollback")
    db_test.update("test").set("remark", "testremark").where(W().equal("id", "18")).result()

# 5)
with db_test.transaction():
    db_test.update("test").set("remark", "1111").where(W().in_("id", [1,5])).result()

# 6)
# with db_test.connection() as conn:
#     db_test.delete("test").where(W().in_("id", [9,10])).result()

# 7)
with db_test.connection() as conn:
    v = db_test.select(*CX("*", None)).from_("test").where(W().equal("id", 7)).value()
    print(v)

# 8)
with db_test.connection() as conn:
    v1 = db_test.select(*CX("COUNT(*)", "COUNT")).from_("test").int()
    print(v1)


class Account():

    def __init__(self, id: int = None, name: str = None, remark: str = None, create_time=None):
        self.id = id
        self.name = name
        self.remark = remark
        self.create_time = create_time

class Account():

    def __init__(self, id: int = None, name: str = None, remark: str = None, create_time=None):
        self.id = id
        self.name = name
        self.remark = remark
        self.create_time = create_time

class Test(Model):
    __table__ = 'test'

    id = IntegerField(primary_key=True)
    name = StringField()
    remark = StringField()
    create_time = DateTimeField()
# 9)
with db_test.connection() as conn:
    v2 = db_test.select(*CX("*", None)).from_("test").where(W().equal("id", 6)).one(Test)
    print(v2)


# 10)
with db_test.connection() as conn:
    v3 = db_test.select(*CX("*", None)).from_("test").list(Test)
    print(v3)

# 11)
with db_test.connection() as conn:
    test = Test(id=11, name="hello world", remark="hello world", create_time=datetime.now())
    db_test.remove(test);

# 12)
with db_test.connection() as conn:
    result = db_test.query(cols=C("id", "name", "remark, create_time")).from_("test").where(W().equal("id", 1)).value()
    print(result)


