from enum import Enum
from typing import List

from bee.db.psd.column import Column


class CriteriaEnum(Enum):
    EQ = 0
    NE = 1
    LT = 2
    LTE = 3
    GT = 4
    GTE = 5
    IN = 6
    NIN = 7
    LK = 8


def pase_criteria_type(type_str: str) -> int:
    if type_str == "" or type_str == "eq":
        return CriteriaEnum.EQ
    elif type_str == "ne":
        return CriteriaEnum.NE
    elif type_str == "lt":
        return CriteriaEnum.LT
    elif type_str == "lte":
        return CriteriaEnum.LTE
    elif type_str == "gt":
        return CriteriaEnum.GT
    elif type_str == "gte":
        return CriteriaEnum.GTE
    elif type_str == "in":
        return CriteriaEnum.IN
    elif type_str == "nin":
        return CriteriaEnum.NIN
    elif type_str == "lk":
        return CriteriaEnum.LK
    else:
        raise TypeError("invalid criteria type: " + type_str)


class Criteria():
    """
    Criteria interface
    """
    pass


class ExprCriteria(str):
    pass


class OneColumnCriteria(Column):
    name = "OneColumnCriteria"

    def __init__(self, col, t: CriteriaEnum, val):
        self.col = col
        self.type = t
        self.value = val


class TwoColumnCriteria(Column):
    name = "TwoColumnCriteria"

    def __init__(self, left: Column, right: Column, t: CriteriaEnum):
        self.left = left
        self.right = right
        self.type = t


class CriteriaSet():
    name = "CriteriaSet"

    def empty(self) -> bool:
        pass


class JoinCriteriaSet(CriteriaSet):
    name = "JoinCriteriaSet"

    def left(self) -> CriteriaSet:
        pass

    def rght(self) -> CriteriaSet:
        pass

    def joiner(self) -> str:
        pass


class NotCriteriaSet(CriteriaSet):
    name = "NotCriteriaSet"

    def __init__(self, inner: CriteriaSet):
        self.inner = inner

    def empty(self) -> bool:
        self.inner.empty()
        return True
def not_(inner: CriteriaSet) -> CriteriaSet:
    return NotCriteriaSet(inner=inner)

class AndCriteriaSet(JoinCriteriaSet):
    name = "AndCriteriaSet"

    def __init__(self, left: CriteriaSet, right: CriteriaSet):
        self.left = left
        self.right = right

    def left(self) -> CriteriaSet:
        return self.left

    def rght(self) -> CriteriaSet:
        return self.right

    def empty(self) -> bool:
        return self.left.empty() and self.right.empty()

    def joiner(self) -> str:
        return "AND"


def and_(left: CriteriaSet, right: CriteriaSet) -> AndCriteriaSet:
    return AndCriteriaSet(left, right)


class OrCriteriaSet(JoinCriteriaSet):
    name = "OrCriteriaSet"

    def __init__(self, left: CriteriaSet, right: CriteriaSet):
        self.left = left
        self.right = right

    def left(self) -> CriteriaSet:
        return self.left

    def rght(self) -> CriteriaSet:
        return self.right

    def empty(self) -> bool:
        return self.left.empty() and self.right.empty()

    def joiner(self) -> str:
        return "OR"


def or_(left: CriteriaSet, right: CriteriaSet) -> OrCriteriaSet:
    return AndCriteriaSet(left, right)


class SimpleCriteriaSet(CriteriaSet):
    name = "SimpleCriteriaSet"

    def __init__(self):
        self.items = []

    def empty(self) -> bool:
        return self.items == None or len(self.items) == 0

    def add(self, col, t: int, val) -> "SimpleCriteriaSet":
        self.items.append(OneColumnCriteria(col, t, val))
        return self

    def add_if(self, when: bool, col, t: int, val) -> "SimpleCriteriaSet":
        if (when):
            self.add(col, t, val)
        return self

    def like(self, col, expr: str) -> "SimpleCriteriaSet":
        return self.add(col, CriteriaEnum.LK, expr)

    def like_if(self, when, col, expr: str) -> "SimpleCriteriaSet":
        return self.add_if(when, col, CriteriaEnum.LK, expr)

    def equal(self, col, val) -> "SimpleCriteriaSet":
        return self.add(col, CriteriaEnum.EQ, val)

    def equal_if(self, when, col, val) -> "SimpleCriteriaSet":
        return self.add_if(when, col, CriteriaEnum.EQ, val)

    def equal2(self, left: CriteriaSet, right: CriteriaSet) -> "SimpleCriteriaSet":
        return self.add2(left, right, CriteriaEnum.EQ)

    def not_equal(self, col, val) -> "SimpleCriteriaSet":
        return self.add(col, CriteriaEnum.EQ, val)

    def not_equal_if(self, when, col, val):
        return self.add_if(when, col, CriteriaEnum.EQ, val)

    def not_equal2(self, left: CriteriaSet, right: CriteriaSet) -> "SimpleCriteriaSet":
        return self.add2(left, right, CriteriaEnum.NE)

    def add2(self, left, right, t: CriteriaEnum) -> "SimpleCriteriaSet":
        item = TwoColumnCriteria(left, right, t)
        self.items.append(item)
        return self

    def in_(self, col, val) -> "SimpleCriteriaSet":
        return self.add(col, CriteriaEnum.IN, val)

    def in_if(self, when, col, val) -> "SimpleCriteriaSet":
        return self.add_if(when, col, CriteriaEnum.IN, val)

    def not_in(self, col, val) -> "SimpleCriteriaSet":
        return self.add(col, CriteriaEnum.NIN, val)

    def not_in_if(self, when, col, val) -> "SimpleCriteriaSet":
        return self.add_if(when, col, CriteriaEnum.NIN, val)

    def less(self, col, val) -> "SimpleCriteriaSet":
        return self.add(col, CriteriaEnum.LT, val)

    def less_if(self, when, col, val) -> "SimpleCriteriaSet":
        return self.add_if(when, col, CriteriaEnum.LT, val)

    def less_or_equal(self, col, val) -> "SimpleCriteriaSet":
        return self.add(col, CriteriaEnum.LTE, val)

    def less_or_equal_if(self, when, col, val) -> "SimpleCriteriaSet":
        return self.add_if(when, col, CriteriaEnum.LTE, val)

    def less2(self, left: CriteriaSet, right: CriteriaSet) -> "SimpleCriteriaSet":
        return self.add(left, right, CriteriaEnum.LT)

    def less_or_equal2(self, left: CriteriaSet, right: CriteriaSet) -> "SimpleCriteriaSet":
        return self.add(left, right, CriteriaEnum.LTE)

    def greater(self, col, val) -> "SimpleCriteriaSet":
        return self.add(col, CriteriaEnum.GT, val)

    def greater_if(self, when, col, val) -> "SimpleCriteriaSet":
        return self.add_if(when, col, CriteriaEnum.GT, val)

    def greater_or_equal(self, col, val) -> "SimpleCriteriaSet":
        return self.add(col, CriteriaEnum.GTE, val)

    def greater_or_equal_if(self, when, col, val) -> "SimpleCriteriaSet":
        return self.add_if(when, col, CriteriaEnum.GTE, val)

    def greater2(self, left: CriteriaSet, right: CriteriaSet) -> "SimpleCriteriaSet":
        return self.add(left, right, CriteriaEnum.GT)

    def greater_or_equal2(self, left: CriteriaSet, right: CriteriaSet) -> "SimpleCriteriaSet":
        return self.add(left, right, CriteriaEnum.GTE)

    def between(self, col, start, end) -> "SimpleCriteriaSet":
        return self.add(col, CriteriaEnum.GTE, start).add(col, CriteriaEnum.LTE, end)

    def prefix(self, col, s) -> "SimpleCriteriaSet":
        return self.like(col, s + "%")

    def suffix(self, col, s) -> "SimpleCriteriaSet":
        return self.like(col, "%" + s)

    def contains(self, col, s) -> "SimpleCriteriaSet":
        return self.like(col, "%" + s + "%")

    def date(self, col, date) -> "SimpleCriteriaSet":
        pass

    def date_range(self, col, start, end) -> "SimpleCriteriaSet":
        pass

def equal(col, val) -> "SimpleCriteriaSet":
    set = SimpleCriteriaSet()
    return set.add(col, CriteriaEnum.EQ, val)