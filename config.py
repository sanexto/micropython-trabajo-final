WIFI_MANAGER_SSID = "ESP"
WIFI_MANAGER_PASSWORD = "trabajofinal"

OTA_URL = "https://raw.githubusercontent.com/sanexto/micropython-trabajo-final/main"
OTA_FILES = [
    "boot.py",
    "config.py",
    "main.py",
    "lib/buzzer.py",
    "lib/fan.py",
    "lib/gas_sensor.py",
    "lib/senko.py",
    "lib/temperature_sensor.py",
    "lib/wifi_manager.py",
]

TEMPERATURE_SENSOR_PIN = 4

GAS_SENSOR_PIN = 34
GAS_SENSOR_THRESHOLD = 512

FAN_IN1_PIN = 26
FAN_IN2_PIN = 27
FAN_ENA_PIN = 25

BUZZER_PIN = 13

READ_INTERVAL = 2
