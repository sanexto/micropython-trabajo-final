import json
from umqtt.simple import MQTTClient


class JSONMQTTClient(MQTTClient):
    ENCODING = "utf-8"

    def set_callback(self, f):
        def wrapper(topic, msg):
            decoded_topic = topic.decode(self.ENCODING)
            decoded_msg = json.loads(msg.decode(self.ENCODING))
            if not isinstance(decoded_msg, dict):
                raise TypeError("msg must be a dict")
            f(decoded_topic, decoded_msg)
        return super().set_callback(wrapper)

    def publish(self, topic, msg, retain=False, qos=0):
        if not isinstance(topic, str):
            raise TypeError("topic must be a string")
        if not isinstance(msg, dict):
            raise TypeError("msg must be a dict")
        encoded_topic = topic.encode(self.ENCODING)
        encoded_msg = json.dumps(msg).encode(self.ENCODING)
        return super().publish(encoded_topic, encoded_msg, retain, qos)

    def subscribe(self, topic, qos=0):
        if not isinstance(topic, str):
            raise TypeError("topic must be a string")
        encoded_topic = topic.encode(self.ENCODING)
        return super().subscribe(encoded_topic, qos)
