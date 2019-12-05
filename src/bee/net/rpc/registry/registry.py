from bee.errors.error import BeeError

class RegistryError(BeeError):
    pass

class Server():

    def __init__(self, protocol: str = None, address: str = None, heartbeat_interval: int = None):
        self.protocol = protocol
        self.address = address
        self.heartbeat_interval = heartbeat_interval


class Registry():

    def register(self, service: str, nid: str, address: str, ttl: int):
        pass

    def deregister(self, service: str, nid: str):
        pass

    def discovery(self, service) -> dict:
        pass

    def close(self):
        pass

