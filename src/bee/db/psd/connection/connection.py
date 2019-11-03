from bee.db.psd.exector import IExecutor
from bee.errors.error import BeeError


class ConnectionError(BeeError):
    pass

class IConnection(IExecutor):

    def exec(self, query, args=[]):
        raise ConnectionError("no effective db connection，please use 'with db.connection() as conn:' syntax")

    def close(self):
        pass

    def begin(self):
        pass

    def commit(self):
        pass

    def rollback(self):
        pass