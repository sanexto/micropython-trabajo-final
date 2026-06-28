import machine

import senko
from wifi_manager import WifiManager

import config


def boot():
    wifi_manager = WifiManager(
        ssid=config.WIFI_MANAGER_SSID,
        password=config.WIFI_MANAGER_PASSWORD,
    )
    wifi_manager.connect()

    print("OTA: Checking for updates...")
    try:
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


if __name__ == "__main__":
    boot()
