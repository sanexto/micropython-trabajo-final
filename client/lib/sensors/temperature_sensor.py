import dht
from machine import Pin


class TemperatureSensor:
    def __init__(self, data_pin):
        self._sensor = dht.DHT22(Pin(data_pin))

    def read(self):
        self._sensor.measure()
        temperature = self._sensor.temperature()
        humidity = self._sensor.humidity()
        return temperature, humidity
