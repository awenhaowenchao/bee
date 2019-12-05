from bee.net.rpc.registry.consul_registry import ConsulRegistry
from bee.net.rpc.registry.etcdv3_registry import Etcd3Registry
from bee.net.rpc.registry.registry import Server as RServer
from bee.net.rpc.server import Server
from bee.net.rpc.transport import Address

etcd = Etcd3Registry(RServer(protocol="etcd3", address="127.0.0.1:2379", heartbeat_interval=30))
srv = Server.new_server(name="test", macher="proto", address=Address(url="127.0.0.1:9000"), registry=etcd)
# server = RServer(protocol="consul", address="127.0.0.1:8500", heartbeat_interval=30)
# cr = ConsulRegistry(server)
# srv = Server.new_server(name="test", macher="json", address=Address(url="127.0.0.1:9000"), registry=cr)

class Test():
    def hello(self, name):
        return "hello " + name

    @classmethod
    def hello1(cls):
        print( "hello")

    @staticmethod
    def hello2(arg1, arg2):
        print("hello")

    def test(self):
        return "test"

srv.register_service(Test())
srv.startup()