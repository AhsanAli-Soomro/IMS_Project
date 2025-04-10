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


class SellingHistory:
    def __init__(self, root):
        self.root = root
        self.root.config(bg="white")


        # Variables
        self.var_search_invoice = StringVar()

        # Title
        title = Label(self.root, text="Selling History", font=("goudy old style", 20, "bold"), bg="#0f4d7d", fg="white")
        title.pack(side=TOP, fill=X)

        # === Search Frame ===
        search_frame = Frame(self.root, bg="white", bd=2, relief=RIDGE)
        search_frame.pack(side=TOP, fill=X, padx=10, pady=10)

        Label(search_frame, text="Invoice No:", font=("goudy old style", 15), bg="white").grid(row=0, column=0, padx=10, pady=10, sticky=W)
        self.txt_invoice = Entry(search_frame, textvariable=self.var_search_invoice, font=("goudy old style", 15), bg="lightyellow")
        self.txt_invoice.grid(row=0, column=1, padx=10, pady=10, sticky=W)

        Button(search_frame, text="Search", command=self.search, font=("goudy old style", 15), bg="#4caf50", fg="white", cursor="hand2").grid(row=0, column=2, padx=10, pady=10)
        Button(search_frame, text="Clear", command=self.clear, font=("goudy old style", 15), bg="#607d8b", fg="white", cursor="hand2").grid(row=0, column=3, padx=10, pady=10)

        # === Table Frame ===
        table_frame = Frame(self.root, bd=3, relief=RIDGE)
        table_frame.pack(fill=BOTH, expand=1, padx=10, pady=(0,10))

        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(table_frame, orient=VERTICAL)

        self.SellingTable = ttk.Treeview(table_frame, columns=(
            "sale_id", "invoice_no", "customer_name", "product_name", 
            "quantity", "selling_price", "total_amount", "discount", "net_pay", "date"),
            yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.SellingTable.xview)
        scroll_y.config(command=self.SellingTable.yview)

        self.SellingTable.pack(fill=BOTH, expand=1)

        # === Table Headings ===
        for col in self.SellingTable["columns"]:
            self.SellingTable.heading(col, text=col.replace("_", " ").title())
            self.SellingTable.column(col, width=100)

        self.SellingTable["show"] = "headings"

        self.show()


    def show(self):
        """Display all sales history."""
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        try:
            cur.execute("SELECT sale_id, invoice_no, customer_name, product_name, quantity, selling_price, total_amount, discount, net_pay, date FROM selling_history ORDER BY sale_id DESC")
            rows = cur.fetchall()
            self.SellingTable.delete(*self.SellingTable.get_children())
            for row in rows:
                self.SellingTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error fetching sales history: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def search(self):
        """Search sales history by invoice number."""
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        try:
            invoice_no = self.var_search_invoice.get().strip()
            if not invoice_no:
                messagebox.showerror("Error", "Please enter an Invoice Number", parent=self.root)
                return

            cur.execute("SELECT sale_id, invoice_no, customer_name, product_name, quantity, selling_price, total_amount, discount, net_pay, date FROM selling_history WHERE invoice_no=?", (invoice_no,))
            rows = cur.fetchall()

            self.SellingTable.delete(*self.SellingTable.get_children())
            if rows:
                for row in rows:
                    self.SellingTable.insert('', END, values=row)
            else:
                messagebox.showerror("Error", "No sales record found for this Invoice!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error searching sales history: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def clear(self):
        """Clear the search field and reload all data."""
        self.var_search_invoice.set("")
        self.show()
