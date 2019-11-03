import contextlib
import types
from queue import Queue

from bee.errors.error import BeeError


class ObjectPool(object):

    def __init__(self, fn_cls, *args, **opts):
        super(ObjectPool, self).__init__()
        self.fn_cls = fn_cls
        self._myinit(*args, **opts)

    def _myinit(self, *args, **kwargs):
        self.queue = Queue()
        self.args = args
        self.min_pool_size = int(kwargs.get("min_pool_size", 0))
        self.max_pool_size = int(kwargs.get("max_pool_size", 5))
        while self.queue.qsize() < self.min_pool_size:
            self.queue.put(self._new())

    def _new(self):
        if type(self.fn_cls) == types.FunctionType:
            if len(self.args) > 0:
                return self.fn_cls(self.args)
            else:
                return self.fn_cls()
        elif type(self.fn_cls) == type:
            return self.fn_cls()
        else:
            raise BeeError("Wrong type")

    @contextlib.contextmanager
    def new(self):
        obj = self.borrow()
        try:
            yield obj
        except BeeError as e:
            yield None
        finally:
            self.recycle(obj)

    def borrow(self):
        if self.queue.qsize() < self.max_pool_size and self.queue.empty():
            self.queue.put(self._new())
        return self.queue.get()

    def recycle(self, obj):
        self.queue.put(obj)
