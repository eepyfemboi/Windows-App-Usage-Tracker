"""
Config.py
"""

import json
import threading


class Config:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.config: dict = ...
            
            #make sure to add any new config values here so that theyre easily accessible in the code
            self.DATABASE_FILE: str = ...
            self.SERVER_PORT: int = ...
            
            self._load_from_file()
            self._unpack_config()
            
            self.initialized = True

    def _load_from_file(self):
        with open("config.json", "r", encoding="utf-8") as f:
            self.config = json.loads(f.read())

    def _unpack_config(self):
        # add new config values here too duh
        self.DATABASE_FILE = self.config.get("DATABASE_FILE", "usage_stats.db")
        self.SERVER_PORT = self.config.get("SERVER_PORT", 33117)
