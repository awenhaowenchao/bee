from sqlite3 import Connection

from bee.db.psd import IConnection


class SqliteConnection(IConnection):
    def __init__(self, conn=Connection()):
        self.conn = conn

    def exec(self, query, *args):
        self.conn

    def find_one(self, query, *args):
        pass

    def find_list(self, query, *args):
        pass

    def close(self):
        self.conn.close()
