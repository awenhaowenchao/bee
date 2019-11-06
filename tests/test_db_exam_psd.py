from datetime import datetime

from bee import Psd, CX, On
from bee import Model, IntegerField, StringField, DateTimeField, Equal, W, C

db_exam = Psd.open("exam")
# 1) sing table count search, SELECT COUNT(*) AS COUNT FROM t_teacher
with db_exam.connection() as conn:
    teacher_count = db_exam.Select(*CX("COUNT(*)", "COUNT")).From("t_teacher").int()
    print("total techer count is %s" % teacher_count)

# 2) sing table search, SELECT * FROM t_teacher
with db_exam.connection() as conn:
    teachers = db_exam.Select(*CX("*")).From("t_teacher").list()
    print(teachers)

# 3) sing table search, SELECT * FROM t_teacher convert values to model of Teacher
class Teacher(Model):
    __table__ = 't_teacher'

    id = IntegerField(primary_key=True)
    name = StringField()

with db_exam.connection() as conn:
    teachers = db_exam.Select(*CX("*")).From("t_teacher").list(Teacher)
    print(teachers)

# 4) sing table search, SELECT * FROM t_teacher WHERE id=? convert values to model of Teacher
with db_exam.connection() as conn:
    teachers = db_exam.Select(*CX("*")).From("t_teacher").Where(W().equal("id", 1004)).list(Teacher)
    print(teachers)

# 5) tow table Join search, SELECT DISTINCT id,cid,score FROM t_student JOIN t_sc ON id=sid WHERE id=?
with db_exam.connection() as conn:
    result = db_exam.Query(C("id", "cid", "score"), True)\
        .From("t_student")\
        .Join("t_sc", On("id", "sid"))\
        .Where(Equal("id", 1001))\
        .list()
    print(result)

# 6) with transaction
with db_exam.transaction():
    # insert sql
    # update sql
    # raise exception
    # update Sql
    pass





