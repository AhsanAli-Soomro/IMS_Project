from tkinter import *
from tkinter import ttk, messagebox
import sqlite3, os, sys

import os, sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller """
    try:
        base_path = sys._MEIPASS  # When running from PyInstaller bundle
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))  # When running normally
    return os.path.join(base_path, relative_path)


DB_PATH = resource_path('ims.db')

class SupplierPurchaseHistory:
    def __init__(self, root):
        self.root = root
        self.root.config(bg="white")

        # === Variables ===
        self.var_search_supplier = StringVar()

        # === Title ===
        title = Label(self.root, text="Supplier Purchase & Update History", font=("goudy old style", 20, "bold"), bg="#0f4d7d", fg="white")
        title.pack(side=TOP, fill=X)

        # === Search Frame ===
        search_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        search_frame.pack(side=TOP, fill=X, padx=10, pady=10)

        Label(search_frame, text="Supplier Name:", font=("goudy old style", 15), bg="white").grid(row=0, column=0, padx=10, pady=5, sticky=W)

        self.cmb_supplier = ttk.Combobox(search_frame, textvariable=self.var_search_supplier, state='readonly', justify=CENTER, font=("goudy old style", 15))
        self.cmb_supplier.grid(row=0, column=1, padx=10, pady=5)
        self.cmb_supplier.set("Select")
        self.fetch_suppliers()

        Button(search_frame, text="Search", command=self.search, font=("goudy old style", 15), bg="#4caf50", fg="white", cursor="hand2").grid(row=0, column=2, padx=10, pady=5)
        Button(search_frame, text="Clear", command=self.clear, font=("goudy old style", 15), bg="#607d8b", fg="white", cursor="hand2").grid(row=0, column=3, padx=10, pady=5)

        # === Table Frame ===
        table_frame = Frame(self.root, bd=3, relief=RIDGE)
        table_frame.pack(fill=BOTH, expand=1, padx=10, pady=(0,10))

        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(table_frame, orient=VERTICAL)

        self.PurchaseTable = ttk.Treeview(table_frame, columns=("Supplier", "Product", "Old Qty", "Added Qty", "New Qty", "Purchase Price", "Total Cost", "Type", "Date"),
                                          yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.PurchaseTable.xview)
        scroll_y.config(command=self.PurchaseTable.yview)

        self.PurchaseTable.pack(fill=BOTH, expand=1)

        # === Table Headings ===
        for col in ["Supplier", "Product", "Old Qty", "Added Qty", "New Qty", "Purchase Price", "Total Cost", "Type", "Date"]:
            self.PurchaseTable.heading(col, text=col)
            self.PurchaseTable.column(col, width=100)

        self.PurchaseTable["show"] = "headings"

        self.show()

    def fetch_suppliers(self):
        """Fetch unique supplier names from the database."""
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        try:
            cur.execute("SELECT DISTINCT Supplier FROM purchase_history")
            suppliers = cur.fetchall()
            self.cmb_supplier['values'] = ["Select"] + [s[0] for s in suppliers]
        except Exception as ex:
            messagebox.showerror("Error", f"Error fetching suppliers: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def show(self):
        """Fetch and display all purchase/update records."""
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        try:
            cur.execute("""
                SELECT Supplier, name, old_qty, added_qty, new_qty, purchase_price, (added_qty * purchase_price) AS total_cost, type, date 
                FROM purchase_history ORDER BY purchase_id DESC
            """)
            rows = cur.fetchall()
            self.PurchaseTable.delete(*self.PurchaseTable.get_children())
            for row in rows:
                self.PurchaseTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error fetching purchase history: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def search(self):
        """Search purchase history for a specific supplier."""
        supplier = self.var_search_supplier.get()
        if supplier == "Select":
            messagebox.showerror("Error", "Please select a supplier", parent=self.root)
            return

        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        try:
            cur.execute("""
                SELECT Supplier, name, old_qty, added_qty, new_qty, purchase_price, (added_qty * purchase_price), type, date 
                FROM purchase_history WHERE Supplier = ? ORDER BY purchase_id DESC
            """, (supplier,))
            rows = cur.fetchall()

            self.PurchaseTable.delete(*self.PurchaseTable.get_children())
            if rows:
                for row in rows:
                    self.PurchaseTable.insert('', END, values=row)
            else:
                messagebox.showinfo("No Data", "No records found for this supplier", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error during search: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def clear(self):
        """Clear the search and reload all data."""
        self.var_search_supplier.set("Select")
        self.show()
