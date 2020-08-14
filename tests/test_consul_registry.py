
from etcd3.events import DeleteEvent

# from bee.data.guid import Guid
# from bee.net.rpc.registry.consul_registry import ConsulRegistry
# from bee.net.rpc.registry.registry import Server

from bee import Guid
from bee.net import ConsulRegistry
from bee.net import RegistryServer as Server

server = Server(protocol="consul", address="127.0.0.1:8500", heartbeat_interval=10)
consulRegistry = ConsulRegistry(server)
consulRegistry.register("test", Guid().string(), "127.0.0.1:8080", "1.0.0", 10)

_result = consulRegistry.discovery("test", ">=1.0.0")
print(_result)



# client = etcd3Registry._etcd
#
# events_iterator, cancel = client.watch_prefix('111', **{})
# client.put('111', '111')
# client.delete('111')
# for event in events_iterator:
#     print(event)
#     t = type(event)
#     if t == DeleteEvent:
#         print("删除")