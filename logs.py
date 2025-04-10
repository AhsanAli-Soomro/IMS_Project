from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class LogsPage(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg="white")

        self.var_search = StringVar()

        # === Title ===
        lbl_title = Label(self, text="User Activity Logs", font=("Arial", 20, "bold"),
                          bg="#0f4d7d", fg="white", bd=10, relief=RIDGE)
        lbl_title.pack(side=TOP, fill=X, padx=10, pady=10, ipady=10)

        # === Search Frame ===
        search_frame = Frame(self, bg="white", bd=2, relief=RIDGE)
        search_frame.pack(fill=X, padx=10, pady=(0, 10))

        lbl_search = Label(search_frame, text="Search by Invoice No or Employee ID:", font=("Arial", 12), bg="white")
        lbl_search.grid(row=0, column=0, padx=10, pady=5, sticky=W)

        txt_search = Entry(search_frame, textvariable=self.var_search, font=("Arial", 12), width=30)
        txt_search.grid(row=0, column=1, padx=10, pady=5, sticky=W)

        btn_search = Button(search_frame, text="Search", command=self.search_logs, font=("Arial", 12), bg="#4caf50", fg="white", cursor="hand2")
        btn_search.grid(row=0, column=2, padx=10, pady=5)

        btn_clear = Button(search_frame, text="Clear", command=self.show_logs, font=("Arial", 12), bg="#607d8b", fg="white", cursor="hand2")
        btn_clear.grid(row=0, column=3, padx=10, pady=5)

        # === Logs Table Frame ===
        logs_frame = Frame(self, bd=3, relief=RIDGE)
        logs_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        scrolly = Scrollbar(logs_frame, orient=VERTICAL)
        scrollx = Scrollbar(logs_frame, orient=HORIZONTAL)

        self.LogsTable = ttk.Treeview(logs_frame, columns=("ID", "Employee ID", "Action", "Invoice No", "Timestamp"),
                                      yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.LogsTable.xview)
        scrolly.config(command=self.LogsTable.yview)

        self.LogsTable.pack(fill=BOTH, expand=True)

        # === Table Headers ===
        self.LogsTable.heading("ID", text="Log ID")
        self.LogsTable.heading("Employee ID", text="Employee ID")
        self.LogsTable.heading("Action", text="Action")
        self.LogsTable.heading("Invoice No", text="Invoice No")
        self.LogsTable.heading("Timestamp", text="Timestamp")
        self.LogsTable["show"] = "headings"

        self.LogsTable.column("ID", width=80, anchor="center")
        self.LogsTable.column("Employee ID", width=150, anchor="center")
        self.LogsTable.column("Action", width=120, anchor="center")
        self.LogsTable.column("Invoice No", width=150, anchor="center")
        self.LogsTable.column("Timestamp", width=200, anchor="center")

        # Load initial logs
        self.show_logs()

    def show_logs(self):
        """Fetch and display all logs."""
        self.var_search.set("")  # Clear search field
        con = sqlite3.connect(os.path.join(BASE_DIR, 'ims.db'))
        cur = con.cursor()
        cur.execute("SELECT id, emp_id, action, COALESCE(invoice_no, 'N/A'), timestamp FROM logs ORDER BY timestamp DESC")
        rows = cur.fetchall()
        self.LogsTable.delete(*self.LogsTable.get_children())
        for row in rows:
            self.LogsTable.insert('', END, values=row)
        con.close()

    def search_logs(self):
        """Search logs by invoice number or employee ID."""
        search_text = self.var_search.get().strip()
        if not search_text:
            messagebox.showerror("Error", "Please enter Invoice No or Employee ID", parent=self)
            return

        con = sqlite3.connect(os.path.join(BASE_DIR, 'ims.db'))
        cur = con.cursor()
        try:
            query = """
                SELECT id, emp_id, action, COALESCE(invoice_no, 'N/A'), timestamp
                FROM logs
                WHERE invoice_no LIKE ? OR emp_id LIKE ?
                ORDER BY timestamp DESC
            """
            cur.execute(query, (f"%{search_text}%", f"%{search_text}%"))
            rows = cur.fetchall()

            self.LogsTable.delete(*self.LogsTable.get_children())
            if rows:
                for row in rows:
                    self.LogsTable.insert('', END, values=row)
            else:
                messagebox.showinfo("No Results", "No logs found for the search criteria.", parent=self)
        except Exception as ex:
            messagebox.showerror("Error", f"Error fetching logs: {str(ex)}", parent=self)
        finally:
            con.close()
