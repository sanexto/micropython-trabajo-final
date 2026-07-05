class MQTTMessage:
    _KEY_ACTION = "action"
    _KEY_DATA = "data"

    def __init__(self, action, data=None):
        if not isinstance(action, str):
            raise TypeError("action must be a string")
        if data is not None and not isinstance(data, dict):
            raise TypeError("data must be a dict")
        self.action = action
        self.data = data

    @classmethod
    def from_dict(cls, msg):
        if not isinstance(msg, dict):
            raise TypeError("msg must be a dict")
        return cls(
            msg.get(cls._KEY_ACTION) or "",
            msg.get(cls._KEY_DATA),
        )

    def to_dict(self):
        return {
            self._KEY_ACTION: self.action,
            self._KEY_DATA: self.data,
        }
