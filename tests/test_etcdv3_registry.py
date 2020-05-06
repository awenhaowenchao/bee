import gevent

from etcd3.events import DeleteEvent

from bee.net.rpc.registry.etcdv3_registry import Etcd3Registry
from bee.net.rpc.registry.registry import Server

server = Server(protocol="etcd3", address="127.0.0.1:2379", heartbeat_interval=10)
etcd3Registry = Etcd3Registry(server)

client = etcd3Registry._etcd

events_iterator, cancel = client.watch_prefix('111', **{})
client.put('111', '111')
client.delete('111')
for event in events_iterator:
    print(event)
    t = type(event)
    if t == DeleteEvent:
        print("删除")