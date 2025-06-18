import sqlite3
import datetime
import os
import sys

# Determine base directory (where the script or exe is located)
def get_db_path():
    """
    Returns the full path to the ims.db file,
    resolving correctly even when bundled with PyInstaller.
    """
    if getattr(sys, 'frozen', False):  # PyInstaller executable
        base_path = os.path.dirname(sys.executable)
    else:  # Running as a script
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, "ims.db")


def log_activity(emp_id, action, invoice_no=None):
    """
    Logs user activities (LOGIN, LOGOUT, BILL_CREATED, etc.) in the logs table.
    """
    con = sqlite3.connect(get_db_path())
    cur = con.cursor()
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur.execute("INSERT INTO logs (emp_id, action, timestamp, invoice_no) VALUES (?, ?, ?, ?)",
                    (emp_id, action, timestamp, invoice_no))
        con.commit()
    except Exception as ex:
        print(f"Error logging action: {str(ex)}")
    finally:
        con.close()


def create_logs_table():
    """
    Creates the 'logs' table in the database if it doesn't exist.
    """
    con = sqlite3.connect(get_db_path())
    cur = con.cursor()
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                emp_id TEXT NOT NULL,
                action TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                invoice_no TEXT DEFAULT NULL
            )
        """)
        con.commit()
    except Exception as ex:
        print(f"Error creating logs table: {str(ex)}")
    finally:
        con.close()


# Automatically ensure logs table exists on import
create_logs_table()
