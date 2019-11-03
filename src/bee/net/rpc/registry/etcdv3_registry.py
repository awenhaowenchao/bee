import etcd3
import gevent
from etcd3 import Etcd3Client

from bee.net.rpc.registry.registry import Registry, Server, RegistryError


class Etcd3Registry(Registry):

    def __init__(self, server: Server):
        self.server = server
        self.etcd = self.registry_factory()

    def registry_factory(self) -> Etcd3Client:
        if self.server == None:
            raise RegistryError("load etcd server error")
        address = self.server.address
        if address:
            return etcd3.client(host=address.split(",")[0].split(":")[0], port=int(address.split(",")[0].split(":")[1]))
        else:
            raise RegistryError("load etcd server error")

    def _svc_key(self, service):
        return '/bee/rpc/{}'.format(service)

    def _node_key(self, service, nid):
        return '/bee/rpc/{}/providers/{}'.format(service, nid)

    def register(self, service: str, nid: str, address: str, ttl: int=None):
        n_key = self._node_key(service, nid)
        ttl = self.server.heartbeat_interval
        self.heartbeat(n_key, address, ttl)

    def deregister(self, service: str, nid: str):
        n_key = self._node_key(service, nid)
        self.etcd.delete(key=n_key)

    # def discovery(self, service) -> List[Node]:
    def discovery(self, service) -> dict:
        s_key = self._svc_key(service)
        res = self.etcd.get_prefix(key_prefix=s_key)
        return {bytes(child[1].key).decode().replace(s_key + "/providers/", "") : bytes(child[0]).decode() for child in res}

        # nodes = []
        # for k, v in {bytes(child[1].key).decode().replace(s_key + "/providers/", ""): bytes(child[0]).decode() for child in res}.items():
        #     node = Node(id=k, address=v)
        #     nodes.append(node)
        # return nodes

    def heartbeat(self, key, value, ttl):
        # print("key=%sm value=%s" % (key, value))
        r = self.etcd.put(key, bytes(value, encoding="utf-8"))

        def heartbeat_loop():
            sleep = int(ttl / 2)
            while 1:
                gevent.sleep(sleep)
                # self.etcd.refresh(key, ttl)
                # TODO: refresh
                self.etcd.put(key, value)

        self.beat_thread = gevent.spawn(heartbeat_loop)

    def watch(self, service, callback):
        def watch_loop():
            s_key = self._svc_key(service)
            # for res in self.etcd.watch(s_key, recursive=True):
            for res in self.etcd.watch(s_key):
                callback({
                    'action': self._proc_action(res.action),
                    'key': res.key,
                    'value': res.value
                })

        self.watch_thread = gevent.spawn(watch_loop)

    def _proc_action(self, action):
        return 'delete' if action == 'expire' else action

    def close(self):
        if hasattr(self, "beat_thread"):
            self.beat_thread.kill()
        if hasattr(self, "watch_thread"):
            self.watch_thread.kill()

def str_to_host(s):
    h, p = s.split(":")
    return (str(h), int(p))