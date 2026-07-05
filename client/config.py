MAIN_LOOP_SLEEP = 50
CHECK_STATUS_INTERVAL = 2000

WIFI_MANAGER_HOSTNAME = "esp-client"
WIFI_MANAGER_SSID = "ESP-CLIENT"
WIFI_MANAGER_PASSWORD = "trabajofinal"

BLUETOOTH_MANAGER_NAME = "ESPC"
BLUETOOTH_MANAGER_SERVICE_UUID = "b2f10000-8a1e-4c9d-9b3a-9f7d6e5c4b3a"
BLUETOOTH_MANAGER_CHAR_TEMPERATURE_UUID = "b2f10001-8a1e-4c9d-9b3a-9f7d6e5c4b3a"
BLUETOOTH_MANAGER_CHAR_HUMIDITY_UUID = "b2f10002-8a1e-4c9d-9b3a-9f7d6e5c4b3a"
BLUETOOTH_MANAGER_CHAR_GAS_UUID = "b2f10003-8a1e-4c9d-9b3a-9f7d6e5c4b3a"
BLUETOOTH_MANAGER_CHAR_FAN_UUID = "b2f10004-8a1e-4c9d-9b3a-9f7d6e5c4b3a"

NTP_HOST = "pool.ntp.org"

MQTT_MANAGER_CLIENT_ID = "esp/client/4cff782b-d80a-4677-95cd-979b17c18e05"
MQTT_MANAGER_SERVER = "broker.hivemq.com"
MQTT_MANAGER_PORT = 1883
MQTT_MANAGER_KEEPALIVE = 60
MQTT_MANAGER_PING_INTERVAL = MQTT_MANAGER_KEEPALIVE * 1000 // 2

MQTT_MANAGER_TOPIC_PREFIX = "sanexto"
MQTT_MANAGER_PUBLISH_TOPIC = f"{MQTT_MANAGER_TOPIC_PREFIX}/{MQTT_MANAGER_CLIENT_ID}"
MQTT_MANAGER_SUBSCRIBE_TOPIC = f"{MQTT_MANAGER_TOPIC_PREFIX}/esp/server/#"

OTA_URL = "https://raw.githubusercontent.com/sanexto/micropython-trabajo-final/main/client"
OTA_FILES = [
    "boot.py",
    "config.py",
    "main.py",
    "lib/actuators/__init__.py",
    "lib/actuators/buzzer.py",
    "lib/actuators/fan.py",
    "lib/bluetooth_manager/__init__.py",
    "lib/bluetooth_manager/bluetooth_manager.py",
    "lib/mqtt/__init__.py",
    "lib/mqtt/json_mqtt_client.py",
    "lib/mqtt/mqtt_manager.py",
    "lib/mqtt/mqtt_message.py",
    "lib/senko/__init__.py",
    "lib/senko/senko.py",
    "lib/sensors/__init__.py",
    "lib/sensors/gas_sensor.py",
    "lib/sensors/temperature_sensor.py",
    "lib/wifi_manager/__init__.py",
    "lib/wifi_manager/wifi_manager.py",
]

TEMPERATURE_SENSOR_PIN = 4

GAS_SENSOR_PIN = 34
GAS_SENSOR_THRESHOLD = 800

FAN_IN1_PIN = 26
FAN_IN2_PIN = 27
FAN_ENA_PIN = 25

BUZZER_PIN = 13
