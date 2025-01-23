"""
Database.py
"""

import sqlite3
import json
import datetime
import threading

from Config import Config

config = Config()

class Database:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.db: sqlite3.Connection = ...
            self.cur: sqlite3.Cursor = ...
            
            self.initialized = True

    def _setup_database(self):
        self.db = sqlite3.connect(config.DATABASE_FILE)
        self.cur = self.db.cursor()
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS app_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                t_hour INTEGER,
                t_day INTEGER,
                t_month INTEGER,
                t_year INTEGER,
                active_app TEXT,
                background_apps TEXT
            )
        ''')
        self.db.commit()

    def _record_usage_entry(self, timestamp: datetime.datetime, active_app: str, background_apps: list[str]):
        self.cur.execute('''
                INSERT INTO app_usage (
                    timestamp, 
                    t_hour, t_day, t_month, t_year, 
                    active_app, background_apps
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''',
            (
                timestamp.isoformat(),
                timestamp.hour,
                timestamp.day,
                timestamp.month,
                timestamp.year,
                active_app,
                json.dumps(background_apps)
            )
        )
        self.db.commit()
