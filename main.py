import time

import config
from buzzer import Buzzer
from fan import Fan
from gas_sensor import GasSensor
from temperature_sensor import TemperatureSensor


def main():
    temperature_sensor = TemperatureSensor(config.TEMPERATURE_SENSOR_PIN)
    gas_sensor = GasSensor(config.GAS_SENSOR_PIN)

    fan = Fan(config.FAN_IN1_PIN, config.FAN_IN2_PIN, config.FAN_ENA_PIN)
    buzzer = Buzzer(config.BUZZER_PIN)

    while True:
        try:
            temperature, humidity = temperature_sensor.read()
            print(f"Temperature: {temperature} C | Humidity: {humidity} %")
        except OSError as e:
            print("Error reading DHT22 sensor:", e)

        gas_value = gas_sensor.read()
        print(f"Gas: {gas_value}")

        if gas_value > config.GAS_SENSOR_THRESHOLD:
            fan.on(Fan.MAX_SPEED)
            print("Fan: ON")
            buzzer.alarm()
        else:
            fan.off()
            print("Fan: OFF")
            buzzer.off()

        time.sleep(config.READ_INTERVAL)


if __name__ == "__main__":
    main()
