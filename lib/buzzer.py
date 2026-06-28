import time
from machine import Pin, PWM

class Buzzer:
    SILENT = 0
    VOLUME = 512

    ALARM_LOW_FREQ = 440
    ALARM_HIGH_FREQ = 880
    ALARM_STEP = 0.05
    ALARM_CYCLES = 5

    def __init__(self, pin):
        self._pwm = PWM(Pin(pin))
        self._pwm.duty(self.SILENT)

    def alarm(self):
        for _ in range(self.ALARM_CYCLES):
            self._tone(self.ALARM_HIGH_FREQ)
            time.sleep(self.ALARM_STEP)
            self._tone(self.ALARM_LOW_FREQ)
            time.sleep(self.ALARM_STEP)
        self.off()

    def off(self):
        self._pwm.duty(self.SILENT)

    def _tone(self, frequency):
        self._pwm.freq(frequency)
        self._pwm.duty(self.VOLUME)
