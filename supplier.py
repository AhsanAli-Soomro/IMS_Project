from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
import os,sys
from SupplierProductPurchaseHistory import SupplierPurchaseHistory # ✅ Import the component
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
class supplierClass(Frame):
    def __init__(self, parent):
        super().__init__(parent)  
        self.configure(bg="white")
        self.pack(fill=BOTH, expand=True)  

        # ------------ Variables --------------
        self.var_searchtxt = StringVar()
        self.var_sup_invoice = StringVar()
        self.var_name = StringVar()
        self.var_contact = StringVar()

        # ------------ Title Label --------------
        Label(self, text="Supplier Management", font=("Arial", 20, "bold"), 
            bg="#0f4d7d", fg="white", padx=20, pady=10).pack(fill=X, anchor=CENTER)

        # ---------- Form Frame -------------
        form_frame = Frame(self, bg="white", bd=2, relief=RIDGE)
        form_frame.place(relx=0.05, rely=0.08, relwidth=0.9, relheight=0.40)  

        # ---------- Define Labels & Fields in Grid Layout -------------
        labels = ["Invoice No.", "Name", "Contact", "Description"]
        input_vars = [self.var_sup_invoice, self.var_name, self.var_contact, None]

        for i in range(3):  
            Label(form_frame, text=labels[i], font=("goudy old style", 15), bg="white").grid(row=i, column=0, padx=10, pady=10, sticky=W)
            Entry(form_frame, textvariable=input_vars[i], font=("goudy old style", 15), bg="lightyellow").grid(row=i, column=1, padx=10, pady=10, sticky=W, ipadx=50)

        # ---------- Description Field -------------
        Label(form_frame, text="Description", font=("goudy old style", 15), bg="white").grid(row=3, column=0, padx=10, pady=10, sticky=W)
        self.txt_desc = Text(form_frame, font=("goudy old style", 15), bg="lightyellow", height=3, width=30)
        self.txt_desc.grid(row=3, column=1, padx=10, pady=10, sticky=W)

        # ---------- Buttons Frame -------------
        btn_frame = Frame(self, bg="white")
        btn_frame.place(relx=0.20, rely=0.52, relwidth=0.6, height=50)

        buttons = [
            ("Save", self.add, "#2196f3"),
            ("Update", self.update, "#4caf50"),
            ("Delete", self.delete, "#f44336"),
            ("Clear", self.clear, "#607d8b"),
        ]

        for i, (text, cmd, color) in enumerate(buttons):
            Button(btn_frame, text=text, command=cmd, font=("goudy old style", 15),
                   bg=color, fg="white", cursor="hand2").grid(row=0, column=i, padx=10, pady=10)

        # ---------- 📌 New Button: View Purchase History ----------
        btn_history = Button(self, text="View Purchase History", command=self.show_purchase_history, 
                            font=("goudy old style", 15, "bold"), bg="#FF9800", fg="white", cursor="hand2")
        btn_history.place(relx=0.35, rely=0.59, relwidth=0.3, height=40)

        # ------------ Supplier Table -------------
        self.create_table()

    def create_table(self):
        """Create the Supplier Table (Responsive)"""
        table_frame = Frame(self, bd=3, relief=RIDGE)
        table_frame.place(relx=0.05, rely=0.65, relwidth=0.9, relheight=0.30)  

        scrolly = Scrollbar(table_frame, orient=VERTICAL)
        scrollx = Scrollbar(table_frame, orient=HORIZONTAL)

        self.SupplierTable = ttk.Treeview(table_frame, columns=("invoice", "name", "contact", "desc"),
                                          yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.SupplierTable.xview)
        scrolly.config(command=self.SupplierTable.yview)

        for col in self.SupplierTable["columns"]:
            self.SupplierTable.heading(col, text=col.upper())
            self.SupplierTable.column(col, width=100)

        self.SupplierTable["show"] = "headings"
        self.SupplierTable.pack(fill=BOTH, expand=True)
        self.SupplierTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()
#-----------------------------------------------------------------------------------------------------
    def add(self):
        con = sqlite3.connect(resource_path("ims.db"))  # ✅ Uses the correct path
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","Invoice must be required",parent=self)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Invoice no. is already assigned",parent=self)
                else:
                    cur.execute("insert into supplier(invoice,name,contact,desc) values(?,?,?,?)",(
                        self.var_sup_invoice.get(),
                        self.var_name.get(),
                        self.var_contact.get(),
                        self.txt_desc.get('1.0',END),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Supplier Added Successfully",parent=self)
                    self.clear()
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def show_purchase_history(self):
        """Opens the SupplierProductPurchaseHistory component over the Supplier UI"""
        # self.destroy()  # Hide the current frame
        new_win = Toplevel(self.master)
        SupplierPurchaseHistory(new_win)

    def show(self):
        con = sqlite3.connect(resource_path("ims.db"))  # ✅ Uses the correct path
        cur=con.cursor()
        try:
            cur.execute("select * from supplier")
            rows=cur.fetchall()
            self.SupplierTable.delete(*self.SupplierTable.get_children())
            for row in rows:
                self.SupplierTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def get_data(self,ev):
        f=self.SupplierTable.focus()
        content=(self.SupplierTable.item(f))
        row=content['values']
        self.var_sup_invoice.set(row[0])
        self.var_name.set(row[1])
        self.var_contact.set(row[2])
        self.txt_desc.delete('1.0',END)
        self.txt_desc.insert(END,row[3])

    def update(self):
        con = sqlite3.connect(resource_path("ims.db"))  # ✅ Uses the correct path
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","Invoice must be required",parent=self)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Invoice No.",parent=self)
                else:
                    cur.execute("update supplier set name=?,contact=?,desc=? where invoice=?",(
                        self.var_name.get(),
                        self.var_contact.get(),
                        self.txt_desc.get('1.0',END),
                        self.var_sup_invoice.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Supplier Updated Successfully",parent=self)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def delete(self):
        con = sqlite3.connect(resource_path("ims.db"))  # ✅ Uses the correct path
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","Invoice No. must be required",parent=self)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Invoice No.",parent=self)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self)
                    if op==True:
                        cur.execute("delete from supplier where invoice=?",(self.var_sup_invoice.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Supplier Deleted Successfully",parent=self)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def clear(self):
        self.var_sup_invoice.set("")
        self.var_name.set("")
        self.var_contact.set("")
        self.txt_desc.delete('1.0',END)
        self.var_searchtxt.set("")
        self.show()

    def search(self):
        con = sqlite3.connect(resource_path("ims.db"))  # ✅ Uses the correct path
        cur=con.cursor()
        try:
            if self.var_searchtxt.get()=="":
                messagebox.showerror("Error","Invoice No. should be required",parent=self)
            else:
                cur.execute("select * from supplier where invoice=?",(self.var_searchtxt.get(),))
                row=cur.fetchone()
                if row!=None:
                    self.SupplierTable.delete(*self.SupplierTable.get_children())
                    self.SupplierTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found!!!",parent=self)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")
