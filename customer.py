from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3,sys,os
import os, sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller """
    try:
        base_path = sys._MEIPASS  # When running from PyInstaller bundle
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))  # When running normally
    return os.path.join(base_path, relative_path)


DB_PATH = resource_path('ims.db')  # ✅ Ensures correct path in .exe
con = sqlite3.connect(DB_PATH)
class CustomerClass(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg="white")
        self.pack(fill=BOTH, expand=True)  # ✅ Ensure the frame expands dynamically

        # ----------- All Variables ------------
        self.var_searchtxt = StringVar()
        self.var_cust_id = StringVar()
        self.var_name = StringVar()
        self.var_email = StringVar()
        self.var_contact = StringVar()

        # ---------- Title Label ----------
        Label(self, text="Customer Management", font=("Arial", 20, "bold"), 
            bg="#0f4d7d", fg="white", padx=20, pady=10).pack(fill=X, anchor=CENTER)

        # ---------- Form Frame -------------
        form_frame = Frame(self, bg="white", bd=2, relief=RIDGE)
        form_frame.place(relx=0.05, rely=0.08, relwidth=0.9, relheight=0.40)  # ✅ Adjusts to all screens

        # ---------- Labels & Fields in Grid Layout -------------
        labels = ["Customer ID:", "Name:", "Email:", "Contact:", "Address:"]
        input_vars = [self.var_cust_id, self.var_name, self.var_email, self.var_contact, None]

        for i in range(4):  # ✅ Creating 4 rows
            Label(form_frame, text=labels[i], font=("goudy old style", 15), bg="white").grid(row=i, column=0, padx=10, pady=10, sticky=W)
            Entry(form_frame, textvariable=input_vars[i], font=("goudy old style", 15), bg="lightyellow").grid(row=i, column=1, padx=10, pady=10, sticky=W, ipadx=50)

        # ---------- Address Field -------------
        Label(form_frame, text="Address", font=("goudy old style", 15), bg="white").grid(row=4, column=0, padx=10, pady=10, sticky=W)
        self.txt_address = Text(form_frame, font=("goudy old style", 15), bg="lightyellow", height=3, width=30)
        self.txt_address.grid(row=4, column=1, padx=10, pady=10, sticky=W)

        # ---------- Buttons Frame -------------
        btn_frame = Frame(self, bg="white")
        btn_frame.place(relx=0.25, rely=0.52, relwidth=0.5, height=50)

        buttons = [
            ("Save", self.add, "#2196f3"),
            ("Update", self.update, "#4caf50"),
            ("Delete", self.delete, "#f44336"),
            ("Clear", self.clear, "#607d8b"),
        ]

        for i, (text, cmd, color) in enumerate(buttons):
            Button(btn_frame, text=text, command=cmd, font=("goudy old style", 15),
                   bg=color, fg="white", cursor="hand2").grid(row=0, column=i, padx=10, pady=10)

        # ---------- Search Bar -------------
        search_frame = Frame(self, bg="white")
        search_frame.place(relx=0.05, rely=0.60, relwidth=0.9, height=50)

        Label(search_frame, text="Customer ID:", font=("goudy old style", 15), bg="white").grid(row=0, column=0, padx=10, pady=10)
        Entry(search_frame, textvariable=self.var_searchtxt, font=("goudy old style", 15), bg="lightyellow").grid(row=0, column=1, padx=10, pady=10, ipadx=50)

        Button(search_frame, text="Search", command=self.search, font=("goudy old style", 15),
               bg="#4caf50", fg="white", cursor="hand2").grid(row=0, column=2, padx=10, pady=10)

        Button(search_frame, text="Show All", command=self.show, font=("goudy old style", 15),
               bg="#ff9800", fg="white", cursor="hand2").grid(row=0, column=3, padx=10, pady=10)

        # ------------ Customer Table -------------
        self.create_table()

    def create_table(self):
        """Create the Customer Table (Responsive)"""
        table_frame = Frame(self, bd=3, relief=RIDGE)
        table_frame.place(relx=0.05, rely=0.70, relwidth=0.9, relheight=0.25)  # ✅ Adjusts dynamically

        scrolly = Scrollbar(table_frame, orient=VERTICAL)
        scrollx = Scrollbar(table_frame, orient=HORIZONTAL)

        self.CustomerTable = ttk.Treeview(table_frame, columns=("id", "name", "email", "contact", "address"),
                                          yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.CustomerTable.xview)
        scrolly.config(command=self.CustomerTable.yview)

        for col in self.CustomerTable["columns"]:
            self.CustomerTable.heading(col, text=col.upper())
            self.CustomerTable.column(col, width=100)

        self.CustomerTable["show"] = "headings"
        self.CustomerTable.pack(fill=BOTH, expand=True)
        self.CustomerTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    # ---------- Database Functions ----------
    def add(self):
        con = sqlite3.connect(resource_path("ims.db"))  # ✅ Uses the correct path
        cur = con.cursor()
        try:
            if self.var_name.get() == "" or self.var_contact.get() == "":
                messagebox.showerror("Error", "Name and Contact are required", parent=self)
            else:
                cur.execute("INSERT INTO customer (name, email, contact, address) VALUES (?, ?, ?, ?)", (
                    self.var_name.get(),
                    self.var_email.get(),
                    self.var_contact.get(),
                    self.txt_address.get('1.0', END),
                ))
                con.commit()
                messagebox.showinfo("Success", "Customer Added Successfully", parent=self)
                self.show()  # Refresh the table after adding a new customer
                self.clear()  # Clear input fields after adding

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self)


    def show(self):
        if not hasattr(self, 'CustomerTable'):  # Prevents errors if table is not initialized
            return

        con = sqlite3.connect(resource_path("ims.db"))  # ✅ Uses the correct path
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM customer")  # Fetch all customer data
            rows = cur.fetchall()
            
            self.CustomerTable.delete(*self.CustomerTable.get_children())  # Clear old data
            for row in rows:
                self.CustomerTable.insert('', END, values=row)  # Insert data into Treeview
            self.var_searchtxt.set("")  # ✅ Reset search field when showing all

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self)



    def get_data(self, ev):
        f = self.CustomerTable.focus()
        content = (self.CustomerTable.item(f))
        row = content['values']
        if row:
            self.var_cust_id.set(row[0])
            self.var_name.set(row[1])
            self.var_email.set(row[2])
            self.var_contact.set(row[3])
            self.txt_address.delete('1.0', END)
            self.txt_address.insert(END, row[4])


    def delete(self):
        con = sqlite3.connect(resource_path("ims.db"))  # ✅ Uses the correct path

        cur = con.cursor()
        try:
            if self.var_cust_id.get() == "":
                messagebox.showerror("Error", "Customer ID is required", parent=self)
            else:
                cur.execute("SELECT * FROM customer WHERE id=?", (self.var_cust_id.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Customer ID", parent=self)
                else:
                    confirm = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self)
                    if confirm:
                        cur.execute("DELETE FROM customer WHERE id=?", (self.var_cust_id.get(),))
                        con.commit()
                        messagebox.showinfo("Success", "Customer Deleted Successfully", parent=self)
                        self.show()  # Refresh table after deletion
                        self.clear()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self)


    def update(self):
        con = sqlite3.connect(resource_path("ims.db"))  # ✅ Uses the correct path
        cur = con.cursor()
        try:
            if self.var_cust_id.get() == "":
                messagebox.showerror("Error", "Customer ID is required", parent=self)
            else:
                cur.execute("SELECT * FROM customer WHERE id=?", (self.var_cust_id.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Customer ID", parent=self)
                else:
                    cur.execute("UPDATE customer SET name=?, email=?, contact=?, address=? WHERE id=?", (
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_contact.get(),
                        self.txt_address.get('1.0', END),
                        self.var_cust_id.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Customer Updated Successfully", parent=self)
                    self.show()  # Refresh table after update
                    self.clear()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self)


    def clear(self):
        self.var_cust_id.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_contact.set("")
        self.txt_address.delete('1.0', END)  # Clear address text box
        self.var_searchtxt.set("")  # Clear search box
        self.show()  # Refresh table



    def search(self):
        con = sqlite3.connect(resource_path("ims.db"))  # ✅ Uses the correct path

        cur = con.cursor()
        try:
            if self.var_searchtxt.get() == "":
                messagebox.showerror("Error", "Customer ID is required for search", parent=self)
            else:
                cur.execute("SELECT * FROM customer WHERE id=?", (self.var_searchtxt.get(),))
                row = cur.fetchone()
                if row:
                    self.CustomerTable.delete(*self.CustomerTable.get_children())
                    self.CustomerTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found", parent=self)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self)


