import sqlite3
import datetime
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def log_activity(emp_id, action, invoice_no=None):
    """
    Logs user activities (LOGIN, LOGOUT, BILL_CREATED, etc.) in the logs table.
    
    Args:
        emp_id (str): Employee ID of the user performing the action.
        action (str): The action being logged (e.g., LOGIN, LOGOUT, BILL_CREATED).
        invoice_no (str or None): Invoice number if applicable (for BILL_CREATED actions).

    Returns:
        None
    """
    con = sqlite3.connect(database=os.path.join(BASE_DIR, 'ims.db'))
    cur = con.cursor()
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get current timestamp
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
    This is useful to ensure logging works without manual table creation.

    Returns:
        None
    """
    con = sqlite3.connect(database=os.path.join(BASE_DIR, 'ims.db'))
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

# Run table creation once when the module is imported
create_logs_table()
