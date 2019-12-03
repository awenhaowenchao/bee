from gevent.lock import BoundedSemaphore
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.read_preferences import PrimaryPreferred, Secondary, SecondaryPreferred, Nearest, Primary

from bee.data.map import Map
from bee import config

READ_PREFERENCE_PRIMARY = "Primary"
READ_PREFERENCE_PRIMARY_PREFERRED = "PrimaryPreferred"
READ_PREFERENCE_SECONDARY = "Secondary"
READ_PREFERENCE_SECONDARY_PREFERRED = "SecondaryPreferred"
READ_PREFERENCE_NEAREST = "Nearest"


class Options(Map):

    def __init__(self, uri: str = None, max_pool_size: int = 100, min_pool_size: int = 20
                 , socket_time_out: int = 5000, connect_time_out: int = 5000
                 , read_preference: str = READ_PREFERENCE_PRIMARY):
        self.uri = uri
        self.max_pool_size = max_pool_size
        self.min_pool_size = min_pool_size
        self.socket_time_out = socket_time_out
        self.connect_time_out = connect_time_out
        self.read_preference = read_preference


class Client():

    def __init__(self, db: str, c: MongoClient, opts=Options):
        self._db = db
        self._client = c
        self._opts = opts


    def db(self) -> Database:
        return self._client[self._db]

    def coll(self, cool_name: str) -> Collection:
        return self._client[self._db][cool_name]

    def client(self) -> MongoClient:
        return self._client

class Factory():

    def __init__(self):
        self.sem = BoundedSemaphore(1)
        self.clients = Map()

    def open(self, name: str) -> Client:
        self.sem.acquire()
        client = self.clients.get(name)
        if client == None:
            client = self.create(name)
        self.sem.release()
        return client

    def create(self, name: str) -> Client:
        client = self.clients.get(name)
        if client != None:
            return client
        else:
            opts = self.load_options(name)
            if opts == None:
                return
            mode = Primary()
            if opts.read_preference == READ_PREFERENCE_PRIMARY_PREFERRED:
                mode = PrimaryPreferred()
            elif opts.read_preference == READ_PREFERENCE_SECONDARY:
                mode = Secondary()
            elif opts.read_preference == READ_PREFERENCE_SECONDARY_PREFERRED:
                mode = SecondaryPreferred()
            elif opts.read_preference == READ_PREFERENCE_NEAREST:
                mode = Nearest()
            kwargs = {
                "read_preference" : mode,
                "maxPoolSize" : opts.max_pool_size,
                "minPoolSize" : opts.min_pool_size,
                "socketTimeoutMS" : opts.socket_time_out,
                "connectTimeoutMS" : opts.connect_time_out
            }
            _client = MongoClient(host=opts.uri, **kwargs)
            client = Client(db=name, c=_client, opts=opts)
            self.clients.set(name, client)
            return client

    def load_options(self, name) -> Options:
        key = "bee.data.mongo." + name
        if not config.exist(key):
            return None

        opts = Options()
        bee_data_mongo_conf = config.get(key)
        opts.cover(bee_data_mongo_conf)
        return opts
