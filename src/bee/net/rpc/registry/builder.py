from bee.net.rpc.registry.consul_registry import ConsulRegistry
from bee.net.rpc.registry.etcdv3_registry import Etcd3Registry
from bee.net.rpc.registry.registry import Registry, Server


class Builder():

    @staticmethod
    def build(server: Server) -> Registry:
        if server.protocol == "etcd3":
            return Etcd3Registry(server)
        elif server.protocol == "consul":
            return ConsulRegistry(server)
        elif server.protocol == "zookeeper":
            pass