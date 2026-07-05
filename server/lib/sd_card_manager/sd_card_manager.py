import os
from machine import SDCard


class SDCardManager:
    _mount_point = None

    def __init__(self):
        raise TypeError(f"{self.__class__.__name__} cannot be instantiated")

    @classmethod
    def mount(cls, slot, mount_point):
        if cls.is_mounted():
            raise RuntimeError(f"SD Card already mounted at {cls._mount_point}")
        sd_card = SDCard(slot=slot)
        os.mount(sd_card, mount_point)
        cls._mount_point = mount_point

    @classmethod
    def unmount(cls):
        if not cls.is_mounted():
            raise RuntimeError(f"SD Card not mounted at {cls._mount_point}")
        os.umount(cls._mount_point)
        cls._mount_point = None

    @classmethod
    def is_mounted(cls):
        if cls._mount_point is None:
            return False
        try:
            os.statvfs(cls._mount_point)
            return True
        except OSError:
            return False
