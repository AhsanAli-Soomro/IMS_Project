import sqlite3
import os
def create_db():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "ims.db")
    con = sqlite3.connect(database=db_path)
    cur = con.cursor()

    # Create Employee Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS employee(
            eid INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            gender TEXT,
            contact TEXT,
            dob TEXT,
            doj TEXT,
            pass TEXT,
            utype TEXT,
            address TEXT,
            salary TEXT
        )
    """)
    con.commit()

    # Create Supplier Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS supplier(
            invoice INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            contact TEXT,
            desc TEXT
        )
    """)
    con.commit()

    # Create Category Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS category(
            cid INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        )
    """)
    con.commit()

    # Create Product Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS product(
            pid INTEGER PRIMARY KEY AUTOINCREMENT,
            Category TEXT NOT NULL,
            Supplier TEXT NOT NULL,
            name TEXT NOT NULL UNIQUE,
            price REAL NOT NULL CHECK(price >= 0),
            purchase_price REAL NOT NULL CHECK(purchase_price >= 0),
            qty INTEGER NOT NULL CHECK(qty >= 0),
            status TEXT CHECK(status IN ('Active', 'Inactive')) DEFAULT 'Active'
        );
    """)
    con.commit()

    # ✅ Corrected Customer Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS customer(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            contact TEXT NOT NULL,
            address TEXT
        );
    """)
    con.commit()

    # Create Settings Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS settings(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            address TEXT,
            company_email TEXT,
            phone_number TEXT,
            discount TEXT
        )
    """)
    con.commit()

    # ✅ Create Purchase History Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS purchase_history(
            purchase_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            supplier_id INTEGER,
            Supplier TEXT,
            name TEXT,
            old_qty INTEGER,
            added_qty INTEGER,
            new_qty INTEGER,
            purchase_price REAL,
            total_cost REAL,
            type TEXT,
            date TEXT DEFAULT CURRENT_DATE,
            FOREIGN KEY (product_id) REFERENCES product(pid),
            FOREIGN KEY (supplier_id) REFERENCES supplier(invoice)
        );
    """)
    con.commit()
# ✅ Create Selling History Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS selling_history (
            sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_no INTEGER NOT NULL,
            customer_name TEXT NOT NULL,
            product_name TEXT NOT NULL,
            quantity INTEGER NOT NULL CHECK(quantity >= 0),
            selling_price REAL NOT NULL CHECK(selling_price >= 0),
            total_amount REAL NOT NULL CHECK(total_amount >= 0),
            discount REAL DEFAULT 0 CHECK(discount >= 0),  -- ✅ NEW: Discount Column
            net_pay REAL NOT NULL CHECK(net_pay >= 0),  -- ✅ NEW: Net Pay Column
            date TEXT DEFAULT CURRENT_DATE,
            FOREIGN KEY (invoice_no) REFERENCES sales(invoice_no) ON DELETE CASCADE
        );
    """)
    con.commit()

 # ✅ Create Sales Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sales(
            sales_id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_no TEXT UNIQUE NOT NULL,
            customer_name TEXT NOT NULL,
            customer_contact TEXT NOT NULL,
            total_amount REAL NOT NULL,
            discount REAL DEFAULT 0.0,
            net_pay REAL NOT NULL,
            payment_method TEXT NOT NULL DEFAULT 'Cash',  -- ✅ Added Payment Method
            emp_id INTEGER NOT NULL,  -- ✅ Tracks the employee who created the sale
            date TEXT DEFAULT CURRENT_DATE,
            FOREIGN KEY (emp_id) REFERENCES employee(eid)  -- ✅ Links sale to employee
        );
    """)
    con.commit()


        # ✅ Create Logs Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS logs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            emp_id INTEGER NOT NULL,
            action TEXT NOT NULL,
            invoice_no TEXT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (emp_id) REFERENCES employee(eid)
        );
    """)
    con.commit()


    # Insert Default Company Settings if Not Exists
    cur.execute("SELECT * FROM settings")
    settings_exists = cur.fetchone()

    if not settings_exists:
        cur.execute("""
            INSERT INTO settings (company_name, address, company_email, phone_number, discount)
            VALUES ('My Company', '123 Street, City', 'admin@company.com', '1234567890', 5)
        """)
        con.commit()
        print("Default company settings added!")

    # Insert Default Admin User if Not Exists
    cur.execute("SELECT * FROM employee WHERE name='admin'")
    admin_exists = cur.fetchone()

    if not admin_exists:
        cur.execute("""
            INSERT INTO employee (name, email, gender, contact, dob, doj, pass, utype, address, salary)
            VALUES ('admin', 'admin@admin.com', 'Male', '1234567890', '2000-01-01', '2023-01-01', 'admin', 'Admin', 'Admin Address', '100000')
        """)
        con.commit()
        print("Admin user created successfully!")
    else:
        print("Admin user already exists.")

    con.close()

# Run the function
create_db()
