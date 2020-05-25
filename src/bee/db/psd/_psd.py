from bee.data.map import Map
from bee.db.psd.db import DBOptions, Database
from bee.db.psd.provider.provider import MysqlProvider, MssqlProvider, SqliteProvider
from bee import config


class Factory():
    name = "psd.Factory"
    """
    Connection factory
    """

    def __init__(self, ):
        self.options = {}
        self.dbMap = Map()

    def open(self, name):
        db = self.dbMap.get(name)
        if not db:
            self.init_db(name)
        db = self.dbMap.get(name)
        return db

    def init_db(self, name):
        db = self.dbMap.get(name)
        if db != None:
            return db

        # 加载配置文件，后面需要提炼出来
        self._load_conf_file()

    def _load_conf_file(self):
        be_data_sql_conf = config.get("bee.data.sql")
        for k, v in be_data_sql_conf.items():
            # options = DBOptions(name=k, provider=v["provider"]
            #                     , max_open_conns=v["max_open_conns"], max_idle_conns=v["max_idle_conns"]
            #                     , trace=v["trace"]
            #                     , options=Map.from_dict(v["options"]))
            options = DBOptions()
            options.name = k
            options.cover(Map.from_dict(v))
            self._add_db(k, options)


    def _add_db(self, name, options=DBOptions()):
        print("opts=(name=%s, provider=%s, max_open_conns=%s, max_idle_conns=%s, trace=%s)" % (options.name, options.provider, options.max_open_conns, options.max_idle_conns, options.trace))
        if options != None:
            self.options[name] = options
            self.dbMap[name] = Factory.build_database(options)

    @staticmethod
    def build_database(options=DBOptions()):
        if options != None:
            database = Database(name=options.name)
            database.opts = options
            if options.provider == "mysql":
                database.p = MysqlProvider()
            elif options.provider == "mssql":
                database.p = MssqlProvider()
            elif options.provider == "sqlite":
                database.p = SqliteProvider()
            return database

factory = Factory()
class Psd():

    @staticmethod
    def open(db_name) -> Database:
        db = factory.open(db_name)
        return db




global providers


def register_provider(name, provider_builder):
    global providers
    providers[name] = provider_builder

