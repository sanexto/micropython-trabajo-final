from .json_mqtt_client import JSONMQTTClient


class MQTTManager:
    _clients = {}

    def __init__(self):
        raise TypeError(f"{self.__class__.__name__} cannot be instantiated")

    @classmethod
    def add_client(cls, client_id, server, port, keepalive):
        cls.remove_client(client_id)
        cls._clients[client_id] = JSONMQTTClient(client_id, server, port, keepalive=keepalive)
        return cls._clients[client_id]

    @classmethod
    def get_client(cls, client_id):
        return cls._clients.get(client_id)

    @classmethod
    def remove_client(cls, client_id):
        if client_id in cls._clients:
            try:
                cls._clients[client_id].disconnect()
            except Exception:
                pass
            del cls._clients[client_id]
            return True
        return False

    @classmethod
    def clear_clients(cls):
        for client_id in list(cls._clients):
            cls.remove_client(client_id)
