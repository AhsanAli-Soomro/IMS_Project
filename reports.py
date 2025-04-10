from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import Calendar  # ✅ Import Date Picker
import sqlite3
import pandas as pd
import os,sys
import datetime


import os, sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller """
    try:
        base_path = sys._MEIPASS  # When running from PyInstaller bundle
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))  # When running normally
    return os.path.join(base_path, relative_path)



DB_PATH = resource_path('ims.db')


class ReportsPage:
    def __init__(self, root):
        self.root = root
        self.root.config(bg="white")

        # === Title ===
        title = Label(self.root, text="Reports", font=("times new roman", 30, "bold"), bg="#010c48", fg="white", pady=5)
        title.pack(side=TOP, fill=X)

        # === Frame for Filters ===
        filters_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        filters_frame.place(x=10, y=60, width=1180, height=100)

        Label(filters_frame, text="Filter By:", font=("times new roman", 15, "bold"), bg="white").place(x=10, y=10)

        self.var_from_date = StringVar()
        self.var_to_date = StringVar()

        Button(filters_frame, text="From Date", command=lambda: self.open_calendar(self.var_from_date)).place(x=150, y=10, width=150)
        Button(filters_frame, text="To Date", command=lambda: self.open_calendar(self.var_to_date)).place(x=320, y=10, width=150)

        self.lbl_from_date = Label(filters_frame, textvariable=self.var_from_date, bg="white")
        self.lbl_from_date.place(x=150, y=40)

        self.lbl_to_date = Label(filters_frame, textvariable=self.var_to_date, bg="white")
        self.lbl_to_date.place(x=320, y=40)

        # ✅ Report Type Dropdown
        self.var_report_type = StringVar()
        self.report_dropdown = ttk.Combobox(filters_frame, textvariable=self.var_report_type, font=("times new roman", 12), state="readonly")
        self.report_dropdown['values'] = ("Select", "Sales Report", "Stock Report", "Customer Report", "Employee Logs")
        self.report_dropdown.place(x=480, y=10, width=180)
        self.report_dropdown.current(0)

        # ✅ Search & Export Buttons
        Button(filters_frame, text="Search", command=self.generate_report, font=("times new roman", 12, "bold"), bg="#2196f3", fg="white").place(x=680, y=10, width=100, height=25)
        Button(filters_frame, text="Export", command=self.export_report, font=("times new roman", 12, "bold"), bg="green", fg="white").place(x=800, y=10, width=100, height=25)

        # === Table for Displaying Reports ===
        report_frame = Frame(self.root, bd=3, relief=RIDGE)
        report_frame.place(x=10, y=170, width=1180, height=500)

        scrolly = Scrollbar(report_frame, orient=VERTICAL)
        scrollx = Scrollbar(report_frame, orient=HORIZONTAL)

        self.report_table = ttk.Treeview(report_frame, yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.report_table.xview)
        scrolly.config(command=self.report_table.yview)

        self.report_table.pack(fill=BOTH, expand=1)

        # Load default report
        self.load_sales_report()
    def generate_report(self):
        """Load the selected report based on the report type and date filters."""
        report_type = self.var_report_type.get()
        from_date = self.var_from_date.get()
        to_date = self.var_to_date.get()

        if report_type == "Sales Report":
            self.load_sales_report(from_date, to_date)
        elif report_type == "Stock Report":
            self.load_stock_report()
        elif report_type == "Customer Report":
            self.load_customer_report()
        elif report_type == "Employee Logs":
            self.load_employee_logs(from_date, to_date)
        else:
            messagebox.showerror("Error", "Please select a valid report type", parent=self.root)

    def load_sales_report(self, from_date=None, to_date=None):
        """Fetch sales data and filter by date range."""
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        try:
            query = "SELECT invoice_no, customer_name, total_amount, date FROM sales ORDER BY date DESC"
            params = ()

            if from_date and to_date:
                query = "SELECT invoice_no, customer_name, total_amount, date FROM sales WHERE date BETWEEN ? AND ? ORDER BY date DESC"
                params = (from_date, to_date)

            cur.execute(query, params)
            rows = cur.fetchall()
            self.update_table(rows, ["Invoice No", "Customer Name", "Total Amount", "Date"])
        except Exception as ex:
            messagebox.showerror("Error", f"Error fetching sales data: {str(ex)}", parent=self.root)
        con.close()
    def load_stock_report(self):
        """Fetch stock data from the product table."""
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        try:
            cur.execute("SELECT pid, name, qty, status FROM product ORDER BY qty ASC")
            rows = cur.fetchall()
            self.update_table(rows, ["Product ID", "Product Name", "Quantity", "Status"])
        except Exception as ex:
            messagebox.showerror("Error", f"Error fetching stock data: {str(ex)}", parent=self.root)
        con.close()

    def load_customer_report(self):
        """Fetch customer purchase details."""
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        try:
            cur.execute("SELECT id, name, contact, email, address FROM customer ORDER BY id DESC")
            rows = cur.fetchall()
            self.update_table(rows, ["Customer ID", "Name", "Contact", "Email", "Address"])
        except Exception as ex:
            messagebox.showerror("Error", f"Error fetching customer data: {str(ex)}", parent=self.root)
        con.close()

    def load_employee_logs(self, from_date=None, to_date=None):
        """Fetch employee log details."""
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        try:
            query = "SELECT emp_id, action, timestamp, invoice_no FROM logs ORDER BY timestamp DESC"
            params = ()

            if from_date and to_date:
                query = "SELECT emp_id, action, timestamp, invoice_no FROM logs WHERE date(timestamp) BETWEEN ? AND ? ORDER BY timestamp DESC"
                params = (from_date, to_date)

            cur.execute(query, params)
            rows = cur.fetchall()
            self.update_table(rows, ["Employee ID", "Action", "Timestamp", "Invoice No"])
        except Exception as ex:
            messagebox.showerror("Error", f"Error fetching employee logs: {str(ex)}", parent=self.root)
        con.close()
    def update_table(self, rows, columns):
        """Update the report table with the given rows and columns."""
        self.report_table.delete(*self.report_table.get_children())
        self.report_table["columns"] = columns
        for col in columns:
            self.report_table.heading(col, text=col)
            self.report_table.column(col, width=150)
        for row in rows:
            self.report_table.insert('', END, values=row)

    def export_report(self):
        """Export the displayed report to a CSV file."""
        rows = self.report_table.get_children()
        if not rows:
            messagebox.showerror("Error", "No data to export!", parent=self.root)
            return

        # Extract data from the table
        data = [self.report_table.item(row)['values'] for row in rows]
        
        # Get column headers
        columns = [self.report_table.heading(col)["text"] for col in self.report_table["columns"]]

        # Convert to DataFrame for exporting
        df = pd.DataFrame(data, columns=columns)

        # Define export file path
        file_path = os.path.join(os.getcwd(), f"Report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
        
        # Save to CSV
        df.to_csv(file_path, index=False)

        # Show success message
        messagebox.showinfo("Export Successful", f"Report exported successfully!\nSaved at: {file_path}", parent=self.root)

    def open_calendar(self, field):
        """Open a date picker for selecting dates."""
        top = Toplevel(self.root)
        cal = Calendar(top, selectmode="day", date_pattern="yyyy-mm-dd")
        cal.pack(pady=20)
        Button(top, text="Select Date", command=lambda: [field.set(cal.get_date()), top.destroy()]).pack()