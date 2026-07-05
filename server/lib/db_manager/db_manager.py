import os, time

from simple_db import simple_db


class DBManager:
    _db = None

    def __init__(self):
        raise TypeError(f"{self.__class__.__name__} cannot be instantiated")

    @classmethod
    def open(cls, db_file_path):
        if cls.is_open():
            raise RuntimeError("Database already open")
        directory = db_file_path.rsplit("/", 1)[0]
        cls._makedirs(directory)
        cls._db = simple_db.SimpleDB(db_file_path, auto_commit=False)

    @classmethod
    def close(cls):
        if not cls.is_open():
            raise RuntimeError("Database not open")
        cls._db.close()
        cls._db = None

    @classmethod
    def get(cls):
        if not cls.is_open():
            raise RuntimeError("Database not open")
        return cls._db

    @classmethod
    def is_open(cls):
        return cls._db is not None

    @classmethod
    def generate_id(cls):
        return "{:016d}".format(int(time.time()) * 1000 + time.ticks_ms() % 1000)

    @classmethod
    def _makedirs(cls, directory):
        path = ""
        for part in directory.strip("/").split("/"):
            path += "/" + part
            try:
                os.stat(path)
            except OSError:
                os.mkdir(path)
