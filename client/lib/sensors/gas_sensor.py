from machine import ADC, Pin


class GasSensor:
    def __init__(self, analog_pin):
        self._adc = ADC(Pin(analog_pin))
        self._adc.atten(ADC.ATTN_11DB)
        self._adc.width(ADC.WIDTH_12BIT)

    def read(self):
        return self._adc.read()
