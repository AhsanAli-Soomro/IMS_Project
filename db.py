import os
import sys
import sqlite3

def get_database_path():
    """Returns the correct writable path to ims.db"""
    if getattr(sys, 'frozen', False):  # Running in PyInstaller bundle
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, "ims.db")


DB_PATH = get_database_path()

def get_connection():
    """Returns a new SQLite connection using the correct path"""
    return sqlite3.connect(DB_PATH)
