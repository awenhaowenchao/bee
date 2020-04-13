from bee.data.guid.guid import Guid
from bee.net.rpc.registry.registry import Registry


class DirectRegistry(Registry):
    """Fake Registry"""

    def __init__(self, url: str):
        self.url = url

    def register(self, service: str, nid: str, address: str):
        pass

    def deregister(self, service: str, nid: str):
        pass

    def discovery(self, service):
        url = self.url
        if url:
            node = {Guid().string() : url}
            return node
        return {}
    def watch(self, service, callback):
        pass

    def close(self):
        pass