import time
from machine import Timer

import config
from actuators import Buzzer, Fan
from bluetooth_manager import BluetoothManager
from mqtt import MQTTManager, MQTTMessage
from sensors import GasSensor, TemperatureSensor


class Main:
    _temperature_sensor = None
    _gas_sensor = None
    _fan = None
    _buzzer = None
    _mqtt = None
    _ping_timer = None
    _ping_pending = False
    _status_timer = None
    _status_pending = False

    def __init__(self):
        raise TypeError(f"{self.__class__.__name__} cannot be instantiated")

    @classmethod
    def run(cls):
        cls._setup_sensors()
        cls._setup_actuators()
        cls._setup_mqtt()
        cls._setup_timers()

        while True:
            cls._mqtt.check_msg()
            cls._check_ping()
            cls._check_status()
            time.sleep_ms(config.MAIN_LOOP_SLEEP)

    @classmethod
    def _setup_sensors(cls):
        cls._temperature_sensor = TemperatureSensor(config.TEMPERATURE_SENSOR_PIN)
        cls._gas_sensor = GasSensor(config.GAS_SENSOR_PIN)

    @classmethod
    def _setup_actuators(cls):
        cls._fan = Fan(config.FAN_IN1_PIN, config.FAN_IN2_PIN, config.FAN_ENA_PIN)
        cls._buzzer = Buzzer(config.BUZZER_PIN)

    @classmethod
    def _setup_mqtt(cls):
        cls._mqtt = MQTTManager.get_client(config.MQTT_MANAGER_CLIENT_ID)
        cls._mqtt.set_callback(cls._on_message)

        print("MQTT: Connecting...")
        cls._mqtt.connect()
        print("MQTT: Connected")

        print("MQTT: Subscribing...")
        cls._mqtt.subscribe(config.MQTT_MANAGER_SUBSCRIBE_TOPIC)
        print("MQTT: Subscribed")

    @classmethod
    def _setup_timers(cls):
        cls._ping_timer = Timer(0)
        cls._ping_timer.init(mode=Timer.PERIODIC, period=config.MQTT_MANAGER_PING_INTERVAL, callback=cls._on_ping)

        cls._status_timer = Timer(1)
        cls._status_timer.init(mode=Timer.PERIODIC, period=config.CHECK_STATUS_INTERVAL, callback=cls._on_status)

    @classmethod
    def _on_message(cls, _, msg):
        message = MQTTMessage.from_dict(msg)
        if message.action == "do_something":
            cls._handle_do_something(message.data)
        else:
            print(f"Unknown action: {message.action}")

    @classmethod
    def _handle_do_something(cls, data):
        pass

    @classmethod
    def _on_ping(cls, _):
        cls._ping_pending = True

    @classmethod
    def _check_ping(cls):
        if not cls._ping_pending:
            return
        cls._ping_pending = False
        cls._mqtt.ping()

    @classmethod
    def _on_status(cls, _):
        cls._status_pending = True

    @classmethod
    def _check_status(cls):
        if not cls._status_pending:
            return

        cls._status_pending = False

        temperature, humidity = cls._temperature_sensor.read()
        gas_value = cls._gas_sensor.read()

        if gas_value > config.GAS_SENSOR_THRESHOLD:
            cls._fan.on(Fan.MAX_SPEED)
            cls._buzzer.alarm()
        else:
            cls._fan.off()
            cls._buzzer.off()

        cls._publish_status(temperature, humidity, gas_value, cls._fan.is_on)

    @classmethod
    def _publish_status(cls, temperature, humidity, gas_value, fan_on):
        BluetoothManager.set(
            config.BLUETOOTH_MANAGER_CHAR_TEMPERATURE_UUID,
            f"{temperature:.2f}",
            notify=True,
        )
        BluetoothManager.set(
            config.BLUETOOTH_MANAGER_CHAR_HUMIDITY_UUID,
            f"{humidity:.2f}",
            notify=True,
        )
        BluetoothManager.set(
            config.BLUETOOTH_MANAGER_CHAR_GAS_UUID,
            f"{gas_value:.2f}",
            notify=True,
        )
        BluetoothManager.set(
            config.BLUETOOTH_MANAGER_CHAR_FAN_UUID,
            "ON" if fan_on else "OFF",
            notify=True,
        )

        cls._mqtt.publish(
            config.MQTT_MANAGER_PUBLISH_TOPIC,
            MQTTMessage(
                "publish_status",
                {
                    "temperature": temperature,
                    "humidity": humidity,
                    "gas_value": gas_value,
                    "fan_on": fan_on,
                },
            ).to_dict(),
        )


if __name__ == "__main__":
    Main.run()
