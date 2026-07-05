import machine, network, ntptime, time

import senko
from wifi_manager import WifiManager

import config
from db_manager import DBManager
from mqtt import MQTTManager
from sd_card_manager import SDCardManager


class Boot:
    is_booted = False

    def __init__(self):
        raise TypeError(f"{self.__class__.__name__} cannot be instantiated")

    @classmethod
    def run(cls):
        if cls.is_booted:
            raise RuntimeError(f"{cls.__name__} has already run")

        print("SD Card: Mounting...")
        SDCardManager.mount(config.SD_CARD_SLOT, config.SD_CARD_MOUNT_POINT)
        print(f"SD Card: Mounted at {config.SD_CARD_MOUNT_POINT}")

        print("WiFi: Setting hostname...")
        network.hostname(config.WIFI_MANAGER_HOSTNAME)
        print(f"WiFi: Hostname set to {config.WIFI_MANAGER_HOSTNAME}")

        wifi_manager = WifiManager(
            ssid=config.WIFI_MANAGER_SSID,
            password=config.WIFI_MANAGER_PASSWORD,
        )

        try:
            print("WiFi: Enabling power save...")
            network.WLAN(network.STA_IF).config(pm=network.WLAN.PM_POWERSAVE)
            print("WiFi: Power save enabled")
        except Exception as e:
            print("WiFi: Could not enable power save:", e)

        wifi_manager.connect()

        print("RTC: Syncing time...")
        ntptime.host = config.NTP_HOST
        ntptime.settime()
        print(f"RTC: Time synced ({time.localtime()})")

        try:
            print("OTA: Checking for updates...")
            ota = senko.Senko(
                user=None,
                repo=None,
                url=config.OTA_URL,
                files=config.OTA_FILES,
            )
            if ota.update():
                print("OTA: Update applied. Restarting...")
                machine.reset()
            else:
                print("OTA: Already up to date")
        except Exception as e:
            print("OTA: Could not check for updates:", e)

        print("DB: Opening...")
        DBManager.open(config.DB_FILE_PATH)
        print(f"DB: Opened at {config.DB_FILE_PATH}")

        print("MQTT: Adding client...")
        MQTTManager.add_client(
            config.MQTT_MANAGER_CLIENT_ID,
            config.MQTT_MANAGER_SERVER,
            config.MQTT_MANAGER_PORT,
            config.MQTT_MANAGER_KEEPALIVE,
        )
        print("MQTT: Client added")

        cls.is_booted = True


if __name__ == "__main__":
    Boot.run()
