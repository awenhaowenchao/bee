import logging

import pymysql

from bee.data.map import Map
from bee.db.psd.connection.connection import IConnection

logging.basicConfig(level=logging.INFO)

class MysqlConnection(IConnection):
    def __init__(self, host: str= '127.0.0.1', port: int=3306, user: str="root", password: str="123456", database: str="test", charset="utf8"):
        logging.info("psd > connect mysql:host=%s, port=%s, user=%s, database=%s, charset=%s" % (host, port, user, database, charset))
        conn = pymysql.connect(host=host, port=port, user=str(user),
                               password=str(password), database=database, charset=charset, autocommit=True)
        self.conn = conn
        conn.open

    def exec(self, query, args=[]):
        # self.conn.begin()
        cursor = self.conn.cursor()
        cursor.execute(query.replace("?", "%s"), args)
        # self.conn.commit()

    def find_one(self, query, args=[]):
        cursor = self.conn.cursor()
        cursor.execute(query.replace("?", "%s"), args)
        cols = cursor.description
        result = Map()
        result.set("cols", cols)
        result.set("data", cursor.fetchone())
        return result

    def find_list(self, query, args=[]):
        cursor = self.conn.cursor()
        cursor.execute(query.replace("?", "%s"), args)
        cols = cursor.description
        result = Map()
        result.set("cols", cols)
        result.set("data", cursor.fetchall())
        return result

    def close(self):
        self.conn.close()

    def begin(self):
        self.conn.begin()

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()
