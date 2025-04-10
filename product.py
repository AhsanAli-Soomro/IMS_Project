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
class productClass(Frame):

    def __init__(self, parent):
        super().__init__(parent)  # ✅ Call Frame's constructor
        self.configure(bg="white")  # ✅ Set background color

        #----------- Variables -------------
        self.var_cat = StringVar()
        self.cat_list = []
        self.sup_list = []
        self.fetch_cat_sup()
        self.var_pid = StringVar()
        self.var_sup = StringVar()
        self.var_name = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_status = StringVar()
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()
        self.var_purchase_price = StringVar()

        # ✅ Configure grid layout with 3 rows
        self.grid_rowconfigure(0, weight=0)  # Row 1 - Product Form
        self.grid_rowconfigure(1, weight=0)  # Row 2 - Search Bar (Fixed height)
        self.grid_rowconfigure(2, weight=2)  # Row 3 - Product Table (Expands)
        self.grid_columnconfigure(0, weight=1)  # Make it responsive

        # ------------- Row 1: Product Form (Full Width) ----------------
        product_Frame = Frame(self, bd=2, relief=RIDGE, bg="white")
        product_Frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        title = Label(product_Frame, text="Manage Product Details", font=("Arial", 20, "bold"), bg="#0f4d7d", fg="white", bd=10, relief=RIDGE)
        title.grid(row=0, column=0, columnspan=6, pady=(0, 10), ipady=10, sticky="ew")

        # Make the frame expand full width
        for i in range(6):  # Configure columns for 3 fields per row
            product_Frame.grid_columnconfigure(i, weight=1)

        # Form Fields (Three Fields Per Row)
        form_fields = [
            ("Category", self.var_cat, self.cat_list, 1, 0),
            ("Supplier", self.var_sup, self.sup_list, 2, 0),
            ("Name", self.var_name, None, 3, 0),
            ("Selling Price", self.var_price, None, 1, 2),
            ("Purchasing Price", self.var_purchase_price, None, 2, 2),
            ("Quantity", self.var_qty, None, 3, 2),
            ("Status", self.var_status, ["Active", "Inactive"], 1, 4),
        ]

        for label, var, values, r, c in form_fields:
            lbl = Label(product_Frame, text=label, font=("goudy old style", 13), bg="white")
            lbl.grid(row=r, column=c, padx=5, pady=2, sticky="w")  # Reduced padding

            if values:
                cmb = ttk.Combobox(product_Frame, textvariable=var, values=values, state='readonly', font=("goudy old style", 12))
                cmb.grid(row=r, column=c+1, padx=5, pady=2, sticky="ew")  # Adjusting for grid structure
                cmb.current(0)
            else:
                txt = Entry(product_Frame, textvariable=var, font=("goudy old style", 12), bg="lightyellow")
                txt.grid(row=r, column=c+1, padx=5, pady=2, sticky="ew")

        # Buttons for Product Form (Full Width)
        btn_frame = Frame(product_Frame, bg="white")
        btn_frame.grid(row=4, column=0, columnspan=6, pady=5, sticky="ew")  # Column span for full width

        buttons = [
            ("Save", self.add, "#2196f3"),
            ("Update", self.update, "#4caf50"),
            ("Delete", self.delete, "#f44336"),
            ("Clear", self.clear, "#607d8b"),
        ]

        for i, (text, cmd, color) in enumerate(buttons):
            Button(btn_frame, text=text, command=cmd, font=("goudy old style", 12),
                bg=color, fg="white", cursor="hand2").grid(row=0, column=i, padx=5, pady=2, ipadx=15, sticky="ew")  # Reduced padding

        # Make button frame stretch full width
        btn_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)




        # ------------- Row 2: Search Bar (Middle) ---------------
        SearchFrame = LabelFrame(self, text="Search Product", font=("goudy old style", 12, "bold"), bd=2, relief=RIDGE, bg="white")
        SearchFrame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        cmb_search = ttk.Combobox(SearchFrame, textvariable=self.var_searchby, values=("Select", "Category", "Supplier", "Name"),
                                  state='readonly', font=("goudy old style", 13))
        cmb_search.pack(side=LEFT, padx=10, pady=10)
        cmb_search.current(0)

        txt_search = Entry(SearchFrame, textvariable=self.var_searchtxt, font=("goudy old style", 13), bg="lightyellow")
        txt_search.pack(side=LEFT, padx=10, pady=10, fill=X, expand=True)

        btn_search = Button(SearchFrame, text="Search", command=self.search, font=("goudy old style", 13),
                            bg="#4caf50", fg="white", cursor="hand2")
        btn_search.pack(side=LEFT, padx=10, pady=10)

        # ------------- Row 3: Product Details Table (Bottom) ----------------
        product_frame = Frame(self, bd=3, relief=RIDGE, bg="white")
        product_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        scrolly = Scrollbar(product_frame, orient=VERTICAL)
        scrollx = Scrollbar(product_frame, orient=HORIZONTAL)

        self.ProductTable = ttk.Treeview(product_frame, columns=("pid", "Category", "Supplier", "name", "price", "purchase_price", "qty", "status"),
                                         yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.ProductTable.xview)
        scrolly.config(command=self.ProductTable.yview)

        self.ProductTable.heading("pid", text="P ID")
        self.ProductTable.heading("Category", text="Category")
        self.ProductTable.heading("Supplier", text="Supplier")
        self.ProductTable.heading("name", text="Name")
        self.ProductTable.heading("price", text="Selling Price")
        self.ProductTable.heading("qty", text="Quantity")
        self.ProductTable.heading("status", text="Status")
        self.ProductTable.heading("purchase_price", text="Purchase Price")
        self.ProductTable["show"] = "headings"

        self.ProductTable.column("pid", width=80)
        self.ProductTable.column("Category", width=100)
        self.ProductTable.column("Supplier", width=100)
        self.ProductTable.column("name", width=150)
        self.ProductTable.column("price", width=100)
        self.ProductTable.column("qty", width=80)
        self.ProductTable.column("status", width=100)
        self.ProductTable.column("purchase_price", width=100)

        self.ProductTable.pack(fill=BOTH, expand=True)
        self.ProductTable.bind("<ButtonRelease-1>", self.get_data)
        self.show()
        self.fetch_cat_sup()

#-----------------------------------------------------------------------------------------------------
    def fetch_cat_sup(self):
        self.cat_list.append("Empty")
        self.sup_list.append("Empty")
        con = sqlite3.connect(resource_path("ims.db"))  # ✅ Uses the correct path
        cur=con.cursor()
        try:
            cur.execute("select name from category")
            cat=cur.fetchall()
            if len(cat)>0:
                del self.cat_list[:]
                self.cat_list.append("Select")
                for i in cat:
                    self.cat_list.append(i[0])
            cur.execute("select name from supplier")
            sup=cur.fetchall()
            if len(sup)>0:
                del self.sup_list[:]
                self.sup_list.append("Select")
                for i in sup:
                    self.sup_list.append(i[0])
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    
    
    def add(self):
        con = sqlite3.connect(resource_path("ims.db"))  # ✅ Uses the correct path
        cur = con.cursor()
        try:
            if self.var_cat.get() == "Select" or self.var_sup.get() == "Select":
                messagebox.showerror("Error", "All fields are required", parent=self)
            else:
                cur.execute("SELECT * FROM product WHERE name=?", (self.var_name.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Product already present", parent=self)
                else:
                    # ✅ Insert product into `product` table
                    cur.execute("INSERT INTO product (Category, Supplier, name, price, purchase_price, qty, status) VALUES (?, ?, ?, ?, ?, ?, ?)", (
                        self.var_cat.get(),
                        self.var_sup.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_purchase_price.get(),
                        self.var_qty.get(),
                        self.var_status.get(),
                    ))

                    # ✅ Insert purchase record into `purchase_history`
                    cur.execute("INSERT INTO purchase_history (Supplier, name, old_qty, added_qty, new_qty, purchase_price, total_cost, type, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, date('now'))", 
                                (self.var_sup.get(), self.var_name.get(), 0, self.var_qty.get(), self.var_qty.get(), self.var_purchase_price.get(), int(self.var_qty.get()) * float(self.var_purchase_price.get()), "Purchase"))

                    con.commit()  # ✅ Commit both insertions
                    messagebox.showinfo("Success", "Product Added Successfully", parent=self)
                    self.clear()
                    self.show()  # ✅ Refresh the table
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self)


    def show(self):
        con = sqlite3.connect(resource_path("ims.db"))  # ✅ Uses the correct path
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM product")
            rows = cur.fetchall()
            self.ProductTable.delete(*self.ProductTable.get_children())  # ✅ Clear table first
            for row in rows:
                self.ProductTable.insert('', END, values=row)  # ✅ Reinsert updated data
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self)



    def get_data(self, ev):
        """Handles selection from the product table and maps correct column data."""
        try:
            f = self.ProductTable.focus()
            content = self.ProductTable.item(f)
            row = content.get("values", [])  # ✅ Use .get() to avoid KeyError
            
            if row and len(row) >= 8:  # ✅ Ensure row has enough columns
                self.var_pid.set(row[0])  # ✅ Product ID
                self.var_cat.set(row[1])  # ✅ Category
                self.var_sup.set(row[2])  # ✅ Supplier
                self.var_name.set(row[3])  # ✅ Product Name
                self.var_price.set(row[4])  # ✅ Selling Price
                self.var_purchase_price.set(row[5])  # ✅ Purchase Price
                self.var_qty.set(row[6])  # ✅ Quantity
                self.var_status.set(row[7])  # ✅ Status

            else:
                self.clear()  # ✅ Clear fields if no row is selected

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self)




    def update(self):
        """Update product details and track quantity changes in purchase history."""
        con = sqlite3.connect(resource_path("ims.db"))  # ✅ Uses the correct path
        cur = con.cursor()
        try:
            if self.var_pid.get() == "":
                messagebox.showerror("Error", "Please select a product from the list!", parent=self)
                return

            cur.execute("SELECT * FROM product WHERE pid=?", (self.var_pid.get(),))
            row = cur.fetchone()
            if row is None:
                messagebox.showerror("Error", "Invalid Product!", parent=self)
                return

            old_qty = int(row[6])  # ✅ Get old quantity
            new_qty = int(self.var_qty.get())  # ✅ New quantity entered
            added_qty = new_qty - old_qty  # ✅ Difference

            # ✅ Update the product table with new quantity and price
            cur.execute("""
                UPDATE product 
                SET Category=?, Supplier=?, name=?, price=?, purchase_price=?, qty=?, status=? 
                WHERE pid=?
            """, (
                self.var_cat.get(),
                self.var_sup.get(),
                self.var_name.get(),
                self.var_price.get(),
                self.var_purchase_price.get(),
                new_qty,  # ✅ Update quantity
                self.var_status.get(),
                self.var_pid.get(),
            ))

            # ✅ Log the update in purchase history if quantity is changed
            if added_qty != 0:
                cur.execute("""
                    INSERT INTO purchase_history (Supplier, name, old_qty, added_qty, new_qty, purchase_price, total_cost, type, date) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, date('now'))
                """, (
                    self.var_sup.get(),
                    self.var_name.get(),
                    old_qty,
                    added_qty,
                    new_qty,
                    self.var_purchase_price.get(),
                    added_qty * float(self.var_purchase_price.get()),
                    "Update"
                ))

            con.commit()  # ✅ Commit all changes to the database
            messagebox.showinfo("Success", "Product Updated Successfully!", parent=self)
            self.show()  # ✅ Refresh the product table
        
        except Exception as ex:
            messagebox.showerror("Error", f"Error updating product: {str(ex)}", parent=self)
        
        finally:
            con.close()




    def delete(self):
        con = sqlite3.connect(resource_path("ims.db"))  # ✅ Uses the correct path
        cur=con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error","Select Product from the list",parent=self)
            else:
                cur.execute("Select * from product where pid=?",(self.var_pid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Product",parent=self)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self)
                    if op==True:
                        cur.execute("delete from product where pid=?",(self.var_pid.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Product Deleted Successfully",parent=self)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def clear(self):
        self.var_cat.set("Select")
        self.var_sup.set("Select")
        self.var_name.set("")
        self.var_price.set("")
        self.var_purchase_price.set("")
        self.var_qty.set("")
        self.var_status.set("Active")
        self.var_pid.set("")
        self.var_searchby.set("Select")
        self.var_searchtxt.set("")
        self.show()

    
    def search(self):
        """Search for a product based on selected criteria safely."""
        con = sqlite3.connect(resource_path("ims.db"))  # ✅ Uses the correct path
        cur = con.cursor()
        try:
            search_by = self.var_searchby.get()
            search_text = self.var_searchtxt.get().strip()

            if search_by == "Select":
                messagebox.showerror("Error", "Please select a search criterion!", parent=self)
                return
            if not search_text:
                messagebox.showerror("Error", "Search input is required!", parent=self)
                return

            query = f"SELECT * FROM product WHERE {search_by} LIKE ?"
            cur.execute(query, ('%' + search_text + '%',))  # ✅ Use parameterized query

            rows = cur.fetchall()
            self.ProductTable.delete(*self.ProductTable.get_children())
            
            if rows:
                for row in rows:
                    self.ProductTable.insert('', END, values=row)
            else:
                messagebox.showinfo("Info", "No matching records found!", parent=self)
        
        except Exception as ex:
            messagebox.showerror("Error", f"Error searching product: {str(ex)}", parent=self)
        
        finally:
            con.close()
