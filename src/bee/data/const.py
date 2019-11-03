# -*- coding: utf-8 -*-
from bee.errors.error import ConstError


class _const:

    def __setattr__(self, key, value):
        if self.__dict__.__contains__(key):
            raise ConstError("can't rebind const (%s)" % key)
        self.__dict__[key] = value


import sys

sys.modules[__name__] = _const()
