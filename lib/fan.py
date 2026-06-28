from machine import Pin, PWM

class Fan:
    MIN_SPEED = 0
    MAX_SPEED = 1023

    def __init__(self, in1_pin, in2_pin, ena_pin):
        self._in1 = Pin(in1_pin, Pin.OUT)
        self._in2 = Pin(in2_pin, Pin.OUT)
        self._ena = PWM(Pin(ena_pin), freq=1000)
        self._in1.value(1)
        self._in2.value(0)
        self._ena.duty(self.MIN_SPEED)

    def on(self, speed):
        self._ena.duty(speed)

    def off(self):
        self._ena.duty(self.MIN_SPEED)
