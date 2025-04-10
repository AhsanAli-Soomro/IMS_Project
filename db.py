import os
import sys
import sqlite3

def get_database_path():
    """Get the correct database path inside PyInstaller .exe/.app"""
    if getattr(sys, 'frozen', False):  # If running as an EXE
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")  # Running in normal mode

    return os.path.join(base_path, "ims.db")

DB_PATH = get_database_path()

def get_connection():
    """Returns a new SQLite database connection"""
    return sqlite3.connect(DB_PATH)
