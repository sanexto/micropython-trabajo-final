MAIN_LOOP_SLEEP = 50

SD_CARD_SLOT = 1
SD_CARD_MOUNT_POINT = "/sd"

DB_FILE_PATH = f"{SD_CARD_MOUNT_POINT}/db/dashboard.db"

WIFI_MANAGER_HOSTNAME = "esp-server"
WIFI_MANAGER_SSID = "ESP-SERVER"
WIFI_MANAGER_PASSWORD = "trabajofinal"

NTP_HOST = "pool.ntp.org"

MQTT_MANAGER_CLIENT_ID = "esp/server/b5e35b0b-a0e9-42ba-93d0-52f49d774686"
MQTT_MANAGER_SERVER = "broker.hivemq.com"
MQTT_MANAGER_PORT = 1883
MQTT_MANAGER_KEEPALIVE = 60
MQTT_MANAGER_PING_INTERVAL = MQTT_MANAGER_KEEPALIVE * 1000 // 2

MQTT_MANAGER_TOPIC_PREFIX = "sanexto"
MQTT_MANAGER_PUBLISH_TOPIC = f"{MQTT_MANAGER_TOPIC_PREFIX}/{MQTT_MANAGER_CLIENT_ID}"
MQTT_MANAGER_SUBSCRIBE_TOPIC = f"{MQTT_MANAGER_TOPIC_PREFIX}/esp/client/#"

OTA_URL = "https://raw.githubusercontent.com/sanexto/micropython-trabajo-final/main/server"
OTA_FILES = [
    "boot.py",
    "config.py",
    "main.py",
    "lib/db_manager/__init__.py",
    "lib/db_manager/db_manager.py",
    "lib/microdot/__init__.py",
    "lib/microdot/asgi.py",
    "lib/microdot/auth.py",
    "lib/microdot/cors.py",
    "lib/microdot/csrf.py",
    "lib/microdot/helpers.py",
    "lib/microdot/jinja.py",
    "lib/microdot/login.py",
    "lib/microdot/microdot.py",
    "lib/microdot/multipart.py",
    "lib/microdot/session.py",
    "lib/microdot/sse.py",
    "lib/microdot/test_client.py",
    "lib/microdot/utemplate.py",
    "lib/microdot/websocket.py",
    "lib/microdot/wsgi.py",
    "lib/mqtt/__init__.py",
    "lib/mqtt/json_mqtt_client.py",
    "lib/mqtt/mqtt_manager.py",
    "lib/mqtt/mqtt_message.py",
    "lib/sd_card_manager/__init__.py",
    "lib/sd_card_manager/sd_card_manager.py",
    "lib/senko/__init__.py",
    "lib/senko/senko.py",
    "lib/simple_db/__init__.py",
    "lib/simple_db/simple_db.py",
    "lib/utemplate/__init__.py",
    "lib/utemplate/compiled.py",
    "lib/utemplate/recompile.py",
    "lib/utemplate/source.py",
    "lib/wifi_manager/__init__.py",
    "lib/wifi_manager/wifi_manager.py",
    "static/dashboard.js",
    "static/logs.js",
    "static/style.css",
    "templates/dashboard.html",
    "templates/footer.html",
    "templates/header.html",
    "templates/logs.html",
]

READING_HISTORY_LIMIT = 20
