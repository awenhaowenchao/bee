from typing import Dict

from typing_extensions import KT, VT


class Map(Dict[KT, VT]):

    def __init__(self, names=(), values=(), **kw):
        super(Map, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key: str):
        self._check_key_type(key)
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Map' object has no attribute '%s'" % key)

    def __setattr__(self, key: str, value):
        self._check_key_type(key)
        self[key] = value

    def __delattr__(self, item):
        del self[item]

    def set(self, key, value):
        self._check_key_type(key)
        self[key] = value

    def get(self, key: str) -> VT:
        self._check_key_type(key)
        if self.contains(key):
            return self[key]
        else:
            return None

    def find(self, key: str):
        if self.contains(key):
            return self.get(key)

        i = key.find(".")
        while i != -1:
            v = self.get(key[:i])
            if v != None:
                tmp, ok = self.try_convert(v)
                # print("k=%s, v=%s, k2=%s, ok=%s" % (key[:i], str(tmp), key[i+1:], str(ok)))
                if ok:
                    return tmp.find(key[i+1:])
            else:
                return None
        return None


    def _check_key_type(self, key: str):
        if isinstance(key, str) == False:
            raise TypeError("args'type %s is not str" % str(type(key)))

    def remove(self, key):
        self._check_key_type(key)
        delattr(self, key)

    def keys(self):
        return list(map(lambda x: x[0], self.items()))

    def values(self):
        return list(map(lambda x: x[1], self.items()))

    def contains(self, key: str):
        self._check_key_type(key)
        return self.keys().__contains__(key)

    def merge(self, src: "Map"):
        for k, v in src.items():
            if self.contains(k):
                tv = self.get(k)
                m1, ok1 = self.try_convert(tv)
                m2, ok2 = self.try_convert(v)
                if ok1 and ok2:
                    m1.merge(m2)
            else:
                tm, ok = self.try_convert(v)
                if ok:
                    self.set(k, tm)
                else:
                    self.set(k, v)

    def cover(self, src: "Map"):
        for k, v in src.items():
            if self.contains(k):
                tv = self.get(k)
                self.set(k, v)
                if tv == None:
                    self.set(k, v)
                else:
                    m1, ok1 = self.try_convert(tv)
                    m2, ok2 = self.try_convert(v)
                    if ok1 and ok2:
                        m1.cover(m2)
            else:
                tm, ok = self.try_convert(v)
                if ok:
                    self.set(k, tm)
                else:
                    self.set(k, v)


    def try_convert(self, i) -> ("Map", bool):
        t = type(i)
        if t == type(self):
            return i, True
        elif t == dict:
            return Map.from_dict(i), True

        return None, False


    def empty(self):
        for x in self.keys():
            delattr(self, x)

    @staticmethod
    def from_dict(d={}):
        map = Map()
        if d != None:
            for k, v in d.items():
                if isinstance(v, dict):
                    map.set(str(k), Map.from_dict(v))
                else:
                    map.set(str(k), v)
        return map

    def __missing__(self, key):
        value = self[key] = type(self)()
        return value
