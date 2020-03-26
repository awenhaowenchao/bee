from typing import List

import redis
from redis import Redis
from redis.sentinel import Sentinel
from rediscluster import RedisCluster
from gevent.lock import BoundedSemaphore

from bee.data.map import Map
from bee import config

TYPE_SINGLE = "single"
TYPE_SENTINEL = "sentinel"
TYPE_CLUSTER = "cluster"


class Options(Map):

    def __init__(self, _type: str = None, address: List[str] = [], password: str = None
                 , socket_connect_timeout: int = 5000, socket_timeout: int = 5000, pool_size: int = None
                 , master: str = None, db: int = 0):
        self.type = _type
        self.address = address
        self.password = password
        self.socket_connect_timeout = socket_connect_timeout
        self.socket_timeout = socket_timeout
        self.pool_size = pool_size
        self.master = master
        self.db = db


class Client():

    def __init__(self, r: object = None, s: Sentinel = None, rc: RedisCluster = None, opts: Options = None):
        self._redis = r
        self._sentinel = s
        self._rc = rc
        self._opts = opts

    def writer(self) -> Redis:
        if self._opts.type == TYPE_SINGLE:
            return self._redis
        elif self._opts.type == TYPE_SENTINEL:
            return self._sentinel.master_for(self._opts.master, password=self._opts.password, db=self._opts.db
                                             , socket_timeout=self._opts.socket_timeout / 1000, socket_connect_timeout=self._opts.socket_connect_timeout / 1000)
        elif self._opts.type == TYPE_CLUSTER:
            return self._rc
        else:
            return None

    def reader(self) -> Redis:
        if self._opts.type == TYPE_SINGLE:
            return self._redis
        elif self._opts.type == TYPE_SENTINEL:
            return self._sentinel.slave_for(self._opts.master, password=self._opts.password, db=self._opts.db
                                            , socket_timeout=self._opts.socket_timeout / 1000, socket_connect_timeout=self._opts.socket_connect_timeout / 1000)
        elif self._opts.type == TYPE_CLUSTER:
            return self._rc
        else:
            return None


class Factory():

    def __init__(self):
        self.sem = BoundedSemaphore(1)
        self.cmds = Map()

    def open(self, name: str) -> Client:
        self.sem.acquire()
        client = self.cmds.get(name)
        if client == None:
            client = self.create(name)
        self.sem.release()
        return client

    def create(self, name: str) -> Client:
        client = self.cmds.get(name)
        if client != None:
            return client
        else:
            opts = self.load_options(name)
            if opts == None:
                return None

            if opts.type == TYPE_SINGLE:
                client = self.create_single(opts)
            elif opts.type == TYPE_SENTINEL:
                client = self.create_sentinel(opts)
            elif opts.type == TYPE_CLUSTER:
                client = self.create_cluster(opts)
            else:
                client = self.create_single(opts)
            self.cmds.set(name, client)
            return client

    def load_options(self, name) -> Options:
        key = "bee.data.redis." + name
        if not config.exist(key):
            pass

        opts = Options()

        bee_data_redis_conf = config.get(key)
        opts.cover(bee_data_redis_conf)
        return opts

    def create_single(self, opts: Options) -> Client:

        pair = opts.address[0].split(":")
        pool = redis.ConnectionPool(host=pair[0], port=int(pair[1]), max_connections=opts.pool_size, db=opts.db)
        r = redis.Redis(connection_pool=pool, socket_timeout=opts.socket_timeout / 1000,
                        socket_connect_timeout=opts.socket_connect_timeout / 1000)
        return Client(r=r, opts=opts)

    def create_sentinel(self, opts: Options) -> Client:

        address_array = []
        for x in opts.address:
            pair = x.split(":")
            address_array.append(tuple(pair))

        sentinel = Sentinel(address_array, socket_timeout=5)
        return Client(s=sentinel, opts=opts)

    def create_cluster(self, opts: Options) -> Client:
        startup_nodes = []
        for v in opts.address:
            pair = v.split(":")
            startup_nodes.append({"host": str(pair[0]), "port": pair[1]})
        rc = RedisCluster(startup_nodes=startup_nodes, decode_responses=True, password=opts.password
                          , max_connections=opts.pool_size, max_connections_per_node=20
                          , socket_timeout=opts.socket_timeout / 1000,
                        socket_connect_timeout=opts.socket_connect_timeout / 1000)
        return Client(rc=rc, opts=opts)
