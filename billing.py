from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
from utils import log_activity
import time
import os, sys, sqlite3
import tempfile
import subprocess
import platform
import datetime
import importlib


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(BASE_DIR, "logo", "company_logo.png")


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller."""
    try:
        base_path = sys._MEIPASS  # When running from PyInstaller
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))  # When running normally
    return os.path.join(base_path, relative_path)


DB_PATH = resource_path('ims.db')  # ✅ Ensures correct path in .exe
con = sqlite3.connect(DB_PATH)



class billClass:
    def __init__(self, root, emp_id):
        self.root = root
        self.emp_id = emp_id
        self.root.geometry("1350x700+110+80")
        self.company_name = self.get_company_name()
        self.root.title(f"{self.company_name} | Inventory Management System")
        self.root.resizable(True, True)  # ✅ Now window is resizable
        self.root.config(bg="white")
        self.cart_list = []
        self.chk_print = 0

        self.var_cname = StringVar()
        self.var_contact = StringVar()

        # ✅ Fullscreen toggle
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)

        #------------- title --------------
        image = Image.open(image_path)
        resized_image = image.resize((50, 50), Image.LANCZOS)  # Change (50, 50) to your desired size
        self.icon_title = ImageTk.PhotoImage(resized_image)

        # Convert the resized image to PhotoImage
        title_text = f"{self.company_name} Inventory Management System"
        self.title_label = Label(self.root, text=title_text, image=self.icon_title, compound=LEFT,
                      font=("times new roman", 36, "bold"), bg="#010c48", fg="white", anchor="w", padx=20)
        self.title_label.place(x=0, y=0, relwidth=1, height=70)


        #------------ logout button -----------
        btn_logout = Label(self.root, text="Logout", cursor="hand2",
                        font=("times new roman", 15, "bold"), bg="yellow", fg="black",
                        relief=RAISED, padx=10, pady=5)

        # ✅ Add Click Event
        btn_logout.bind("<Button-1>", lambda e: self.logout())  # Simulate button click

        # ✅ Add Hover Effect
        btn_logout.bind("<Enter>", lambda e: btn_logout.config(bg="#FFD700"))  # Darker yellow on hover
        btn_logout.bind("<Leave>", lambda e: btn_logout.config(bg="yellow"))  # Restore original color

        btn_logout.place(relx=0.85, y=10, height=50, width=150)


        #------------ clock -----------------
        self.lbl_clock = Label(self.root, text="Welcome to Inventory Management System",
                               font=("times new roman", 15), bg="#4d636d", fg="white")
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        #------------ footer -----------------
        lbl_footer = Label(self.root, text="IMS-Inventory Management System | Developed by Nishant Gupta\n"
                                           "For any Technical Issues Contact: 9899459288",
                           font=("times new roman", 10), bg="#4d636d", fg="white")
        lbl_footer.pack(side=BOTTOM, fill=X)

        #-------------- product frame -----------------
        ProductFrame1 = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        ProductFrame1.place(relx=0.005, rely=0.15, relwidth=0.3, relheight=0.75)  # ✅ Dynamic placement

        pTitle = Label(ProductFrame1, text="All Products", font=("goudy old style", 20, "bold"),
                       bg="#262626", fg="white")
        pTitle.pack(side=TOP, fill=X)

        self.var_search = StringVar()

        ProductFrame2 = Frame(ProductFrame1, bd=2, relief=RIDGE, bg="white")
        ProductFrame2.place(x=2, y=42, relwidth=0.99, height=90)

        lbl_search = Label(ProductFrame2, text="Search Product | By Name", font=("times new roman", 15, "bold"),
                           bg="white", fg="green").place(x=2, y=5)

        lbl_search = Label(ProductFrame2, text="Product Name", font=("times new roman", 15, "bold"),
                           bg="white").place(x=2, y=45)
        txt_search = Entry(ProductFrame2, textvariable=self.var_search, font=("times new roman", 15),
                           bg="lightyellow").place(x=128, y=47, width=150, height=22)
        btn_search = Button(ProductFrame2, text="Search", command=self.search, font=("goudy old style", 15),
                            bg="#2196f3", fg="white", cursor="hand2").place(x=285, y=45, width=100, height=25)
        btn_show_all = Button(ProductFrame2, text="Show All", command=self.show, font=("goudy old style", 15),
                              bg="#083531", fg="white", cursor="hand2").place(x=285, y=10, width=100, height=25)

        ProductFrame3 = Frame(ProductFrame1, bd=3, relief=RIDGE)
        ProductFrame3.place(x=2, y=140, relwidth=0.99, relheight=0.6)

        scrolly=Scrollbar(ProductFrame3,orient=VERTICAL)
        scrollx=Scrollbar(ProductFrame3,orient=HORIZONTAL)\
        
        self.product_Table=ttk.Treeview(ProductFrame3,columns=("pid","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.product_Table.xview)
        scrolly.config(command=self.product_Table.yview)
        self.product_Table.heading("pid",text="P ID")
        self.product_Table.heading("name",text="Name")
        self.product_Table.heading("price",text="Price")
        self.product_Table.heading("qty",text="Quantity")
        self.product_Table.heading("status",text="Status")
        self.product_Table["show"]="headings"
        self.product_Table.column("pid",width=40)
        self.product_Table.column("name",width=100)
        self.product_Table.column("price",width=100)
        self.product_Table.column("qty",width=40)
        self.product_Table.column("status",width=90)
        self.product_Table.pack(fill=BOTH,expand=1)
        self.product_Table.bind("<ButtonRelease-1>",self.get_data)
        self.show()

        lbl_note=Label(ProductFrame1,text="Note: 'Enter 0 Quantity to remove product from the Cart'",font=("goudy old style",12),anchor="w",bg="white",fg="red").pack(side=BOTTOM,fill=X)

                #-------------- customer frame ---------------
        CustomerFrame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        CustomerFrame.place(relx=0.31, rely=0.15, relwidth=0.35, height=100)

        cTitle = Label(CustomerFrame, text="Customer Details", font=("goudy old style", 15), bg="lightgray")
        cTitle.pack(side=TOP, fill=X)

        self.var_customer = StringVar()
        lbl_select_customer = Label(CustomerFrame, text="Select Customer", font=("times new roman", 13), bg="white")
        lbl_select_customer.place(x=5, y=35)
        self.customer_dropdown = ttk.Combobox(CustomerFrame, textvariable=self.var_customer,
                                              font=("times new roman", 13), state="readonly")
        self.customer_dropdown.place(x=100, y=35, width=180)
        self.customer_dropdown.bind("<<ComboboxSelected>>", self.fill_customer_details)

        # ✅ Manual Input Fields
        lbl_name=Label(CustomerFrame,text="Name",font=("times new roman",13),bg="white").place(x=5,y=65)
        txt_name=Entry(CustomerFrame,textvariable=self.var_cname,font=("times new roman",13),bg="lightyellow").place(x=50,y=65,width=180)

        lbl_contact=Label(CustomerFrame,text="Contact No.",font=("times new roman",13),bg="white").place(x=250,y=65)
        txt_contact=Entry(CustomerFrame,textvariable=self.var_contact,font=("times new roman",13),bg="lightyellow").place(x=330,y=65,width=180)

        # ✅ Load customer data on startup
        self.load_customers()

        # ------------------- Cart and Calculator Frame -------------------
        Cal_Cart_Frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        Cal_Cart_Frame.place(relx=0.31, rely=0.30, relwidth=0.38, relheight=0.46)  # ✅ Adjusted for fullscreen

        # --------------- Calculator Frame ---------------------
        self.var_cal_input = StringVar()

        Cal_Frame = Frame(Cal_Cart_Frame, bd=9, relief=RIDGE, bg="white")
        Cal_Frame.place(relx=0.02, rely=0.02, relwidth=0.48, relheight=0.90)  # ✅ Relative sizing

        self.txt_cal_input = Entry(Cal_Frame, textvariable=self.var_cal_input, font=('arial', 15, 'bold'),
                                width=21, relief=GROOVE, state='readonly', justify=RIGHT)
        self.txt_cal_input.grid(row=0, columnspan=4, sticky="nsew")  # ✅ Expands inside frame

        # Dynamically adjust button size and placement
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('+', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('*', 3, 3),
            ('0', 4, 0), ('C', 4, 1), ('=', 4, 2), ('/', 4, 3)
        ]

        for (text, row, col) in buttons:
            Button(Cal_Frame, text=text, font=('arial', 15, 'bold'),
                command=lambda t=text: self.get_input(t) if t not in ["=", "C"] else (
                    self.perform_cal() if t == "=" else self.clear_cal()),
                 width=4, height=2, pady=3, cursor="hand2")\
                .grid(row=row, column=col, sticky="nsew", padx=2, pady=2)

        # Ensure buttons expand when resized
        for i in range(5):
            Cal_Frame.grid_rowconfigure(i, weight=1)
            Cal_Frame.grid_columnconfigure(i, weight=1)

        # ------------------ Cart Frame (Updated for Responsiveness) --------------------
        Cart_Frame = Frame(Cal_Cart_Frame, bd=3, relief=RIDGE, bg="white")
        Cart_Frame.place(relx=0.52, rely=0.02, relwidth=0.46, relheight=0.90)  # ✅ Dynamically resizable

        # ✅ Title Label (Expands with Frame)
        self.cartTitle = Label(Cart_Frame, text="Total Products: [0]", font=("goudy old style", 15), bg="lightgray")
        self.cartTitle.pack(side=TOP, fill=X)

        # ✅ Define Scrollbars first
        scrolly = Scrollbar(Cart_Frame, orient=VERTICAL)
        scrollx = Scrollbar(Cart_Frame, orient=HORIZONTAL)

        # ✅ Create Cart Table with proper column configuration
        self.CartTable = ttk.Treeview(
            Cart_Frame, 
            columns=("pid", "name", "price", "qty"),
            yscrollcommand=scrolly.set,
            xscrollcommand=scrollx.set
        )

        # ✅ Configure Scrollbars
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.CartTable.xview)
        scrolly.config(command=self.CartTable.yview)

        # ✅ Set Column Headings
        self.CartTable.heading("pid", text="P ID")
        self.CartTable.heading("name", text="Name")
        self.CartTable.heading("price", text="Price")
        self.CartTable.heading("qty", text="Quantity")
        self.CartTable["show"] = "headings"

        # ✅ Adjust Column Widths for Better Scaling
        self.CartTable.column("pid", anchor=CENTER, width=60)
        self.CartTable.column("name", anchor=W, width=120)
        self.CartTable.column("price", anchor=E, width=100)
        self.CartTable.column("qty", anchor=CENTER, width=60)

        # ✅ Pack Table after Defining Everything
        self.CartTable.pack(fill=BOTH, expand=True)

        # ✅ Ensure Table Expands with Frame
        Cart_Frame.grid_rowconfigure(0, weight=1)
        Cart_Frame.grid_columnconfigure(0, weight=1)

        # ✅ Bind event after defining self.CartTable
        self.CartTable.bind("<ButtonRelease-1>", self.get_data_cart)




        #-------------- add cart widgets frame ---------------
        self.var_pid=StringVar()
        self.var_pname=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_stock=StringVar()

        # ------------------- Add Cart Widgets Frame (Improved Layout & Responsiveness) -------------------
        Add_CartWidgets_Frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        Add_CartWidgets_Frame.place(relx=0.31, rely=0.77, relwidth=0.38, relheight=0.18)  # ✅ Fully responsive

        # ✅ Configure Grid for Proper Alignment
        Add_CartWidgets_Frame.grid_columnconfigure((0, 1, 2), weight=1)
        Add_CartWidgets_Frame.grid_rowconfigure((0, 1, 2, 3), weight=1)

        # -------------------- ROW 1: Labels --------------------
        lbl_p_name = Label(Add_CartWidgets_Frame, text="Product Name", font=("times new roman", 12, "bold"), bg="white")
        lbl_p_name.grid(row=0, column=0, padx=5, pady=2, sticky="w")

        lbl_p_price = Label(Add_CartWidgets_Frame, text="Price Per Qty", font=("times new roman", 12, "bold"), bg="white")
        lbl_p_price.grid(row=0, column=1, padx=5, pady=2, sticky="w")

        lbl_p_qty = Label(Add_CartWidgets_Frame, text="Quantity", font=("times new roman", 12, "bold"), bg="white")
        lbl_p_qty.grid(row=0, column=2, padx=5, pady=2, sticky="w")

        # -------------------- ROW 2: Entry Fields --------------------
        txt_p_name = Entry(Add_CartWidgets_Frame, textvariable=self.var_pname, font=("times new roman", 12),
                        bg="lightyellow", state='readonly')
        txt_p_name.grid(row=1, column=0, padx=5, pady=2, sticky="ew")

        txt_p_price = Entry(Add_CartWidgets_Frame, textvariable=self.var_price, font=("times new roman", 12),
                            bg="lightyellow", state='readonly')
        txt_p_price.grid(row=1, column=1, padx=5, pady=2, sticky="ew")

        txt_p_qty = Entry(Add_CartWidgets_Frame, textvariable=self.var_qty, font=("times new roman", 12),
                        bg="lightyellow")
        txt_p_qty.grid(row=1, column=2, padx=5, pady=2, sticky="ew")

        # -------------------- ROW 3: Stock Label --------------------
        self.lbl_inStock = Label(Add_CartWidgets_Frame, text="In Stock", font=("times new roman", 12, "bold"), bg="white")
        self.lbl_inStock.grid(row=2, column=0, columnspan=3, pady=2, sticky="w")

        # -------------------- ROW 4: Buttons (Smaller Size) --------------------
        btn_clear_cart = Button(Add_CartWidgets_Frame, command=self.clear_cart, text="Clear",
                                font=("times new roman", 12, "bold"), bg="lightgray", cursor="hand2", width=8)
        btn_clear_cart.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

        btn_add_cart = Button(Add_CartWidgets_Frame, command=self.add_update_cart, text="Add | Update",
                            font=("times new roman", 12, "bold"), bg="orange", cursor="hand2", width=12)
        btn_add_cart.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky="ew")


        
        #------------------- billing area -------------------
        billFrame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        billFrame.place(relx=0.695, rely=0.15, relwidth=0.300, relheight=0.58)

        BTitle = Label(billFrame, text="Customer Bill Area", font=("goudy old style", 20, "bold"),
                       bg="#262626", fg="white")
        BTitle.pack(side=TOP, fill=X)

        scrolly = Scrollbar(billFrame, orient=VERTICAL)
        scrolly.pack(side=RIGHT, fill=Y)

        self.txt_bill_area = Text(billFrame, yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH, expand=1)
        scrolly.config(command=self.txt_bill_area.yview)            

        #------------------- billing buttons -----------------------
        billMenuFrame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        billMenuFrame.place(relx=0.695, rely=0.75, relwidth=0.315, height=140)

        self.lbl_amnt = Label(billMenuFrame, text="Bill Amount\n[0]", font=("goudy old style", 15, "bold"),
                              bg="#3f51b5", fg="white")
        self.lbl_amnt.place(x=2, y=5, width=120, height=70)

        btn_print = Button(billMenuFrame, text="Print", command=self.print_bill, cursor="hand2",
                           font=("goudy old style", 15, "bold"), bg="lightgreen", fg="white")
        btn_print.place(x=2, y=80, width=120, height=50)

        # ✅ Fetch Discount from Database on Startup
        DB_PATH = resource_path('ims.db')
        con = sqlite3.connect(DB_PATH)

        cur = con.cursor()
        try:
            cur.execute("SELECT discount FROM settings WHERE id=1")
            row = cur.fetchone()
            if row:
                self.discount_rate = float(row[0]) 
                # self.discount_rate = 0 
        except Exception:
            self.discount_rate = 0 
        con.close()

        # ✅ Create UI Labels with Dynamic Discount
        self.lbl_discount = Label(billMenuFrame, text=f"Discount ({self.discount_rate}%)\n[0]", 
                                  font=("goudy old style", 15, "bold"), bg="#8bc34a", fg="white")
        self.lbl_discount.place(x=124, y=5, width=120, height=70)


        self.lbl_net_pay=Label(billMenuFrame,text="Net Pay\n[0]",font=("goudy old style",15,"bold"),bg="#607d8b",fg="white")
        self.lbl_net_pay.place(x=246,y=5,width=160,height=70)

        # Print Button
        btn_print = Label(billMenuFrame, text="Print", cursor="hand2",
                        font=("goudy old style", 15, "bold"), bg="#caff8a", fg="black",
                        relief=RAISED, padx=10, pady=5)

        # ✅ Add Click Event
        btn_print.bind("<Button-1>", lambda e: self.print_bill())  # Simulate button click

        # ✅ Add Hover Effect
        btn_print.bind("<Enter>", lambda e: btn_print.config(bg="#b0e57c"))  # Change color on hover
        btn_print.bind("<Leave>", lambda e: btn_print.config(bg="#caff8a"))  # Restore original color when mouse leaves

        btn_print.place(x=2, y=80, width=120, height=50)

        # Clear Button
        btn_clear_all = Label(billMenuFrame, text="Clear All", cursor="hand2",
                            font=("goudy old style", 15, "bold"), bg="gray", fg="white",
                            relief=RAISED, padx=10, pady=5)

        # ✅ Add Click Event
        btn_clear_all.bind("<Button-1>", lambda e: self.clear_all())  # Simulate button click

        # ✅ Add Hover Effect
        btn_clear_all.bind("<Enter>", lambda e: btn_clear_all.config(bg="#707070"))  # Darker gray on hover
        btn_clear_all.bind("<Leave>", lambda e: btn_clear_all.config(bg="gray"))  # Restore original color

        btn_clear_all.place(x=124, y=80, width=120, height=50)

        # Add Update Button
        btn_generate = Label(billMenuFrame, text="Generate Bill", cursor="hand2",
                            font=("goudy old style", 15, "bold"), bg="#009688", fg="white",
                            relief=RAISED, padx=10, pady=5)

        # ✅ Add Click Event
        btn_generate.bind("<Button-1>", lambda e: self.generate_bill())  # Simulate button click

        # ✅ Add Hover Effect
        btn_generate.bind("<Enter>", lambda e: btn_generate.config(bg="#00796B"))  # Darker shade on hover
        btn_generate.bind("<Leave>", lambda e: btn_generate.config(bg="#009688"))  # Restore original color

        btn_generate.place(x=246, y=80, width=160, height=50)


        self.show()
        self.auto_update_title()
        self.update_date_time()
#---------------------- all functions ------------------------------


    def toggle_fullscreen(self, event=None):
        self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen"))

    def exit_fullscreen(self, event=None):
        self.root.attributes("-fullscreen", False)

    def get_input(self,num):
        xnum=self.var_cal_input.get()+str(num)
        self.var_cal_input.set(xnum)

    def get_company_name(self):
        """Fetch the company name from the settings table."""
        try:
            con = sqlite3.connect(database=os.path.join(BASE_DIR, 'ims.db'))
            cur = con.cursor()
            cur.execute("SELECT company_name FROM settings WHERE id=1")
            row = cur.fetchone()
            con.close()

            if row and row[0]:
                return row[0]  # ✅ Return the stored company name
            else:
                return "Inventory Management"  # ✅ Default name if not found
        except Exception as ex:
            messagebox.showerror("Error", f"Error fetching company name: {str(ex)}", parent=self.root)
            return "Inventory Management"
        
    def update_bill_title(self):
        """Update the bill title when settings change."""
        self.company_name = self.get_company_name()
        title_text = f"{self.company_name} Inventory Management System"
        self.title_label.config(text=title_text)

    def auto_update_title(self):
        """Check for company name updates every 5 seconds."""
        self.update_bill_title()
        self.root.after(5000, self.auto_update_title)

    def log_activity(self, emp_id, action, invoice_no=None):
        """Log user activities in logs table with timestamps and Invoice Number"""
        con = sqlite3.connect(database=os.path.join(BASE_DIR, 'ims.db'))
        cur = con.cursor()
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Correct timestamp format
            cur.execute("INSERT INTO logs (emp_id, action, timestamp, invoice_no) VALUES (?, ?, ?, ?)",
                        (emp_id, action, timestamp, invoice_no))
            con.commit()
        except Exception as ex:
            print(f"Error logging action: {str(ex)}")
        finally:
            con.close()

    def logout(self):
        """Logs out the user and returns to the login screen."""
        self.log_activity(self.emp_id, "LOGOUT")  # ✅ Fixed: Now uses `self.log_activity`

        self.root.destroy()
        login_module = importlib.import_module("login")
        root = Tk()
        login_module.LoginSystem(root)
        root.mainloop()





    def clear_cal(self):
        self.var_cal_input.set('')

    def perform_cal(self):
        try:
            result = eval(self.var_cal_input.get())
            self.var_cal_input.set(result)
        except ZeroDivisionError:
            messagebox.showerror("Error", "Cannot divide by zero!")
            self.var_cal_input.set("")
        except Exception:
            messagebox.showerror("Error", "Invalid Calculation!")
            self.var_cal_input.set("")


    def show(self):
        con = sqlite3.connect(resource_path("ims.db"))  # ✅ Uses the correct path
        cur=con.cursor()
        try:
            cur.execute("select pid,name,price,qty,status from product where status='Active'")
            rows=cur.fetchall()
            self.product_Table.delete(*self.product_Table.get_children())
            for row in rows:
                self.product_Table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def search(self):
        con = sqlite3.connect(resource_path("ims.db"))  # ✅ Uses the correct path
        cur=con.cursor()
        try:
            if self.var_search.get()=="":
                messagebox.showerror("Error","Search input should be required",parent=self.root)
            else:
                cur.execute("select pid,name,price,qty,status from product where name LIKE '%"+self.var_search.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.product_Table.delete(*self.product_Table.get_children())
                    for row in rows:
                        self.product_Table.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found!!!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def get_data(self,ev):
        f=self.product_Table.focus()
        content=(self.product_Table.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_inStock.config(text=f"In Stock [{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_qty.set('1')
    
    def get_data_cart(self,ev):
        f=self.CartTable.focus()
        content=(self.CartTable.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set(row[3])
        self.lbl_inStock.config(text=f"In Stock [{str(row[4])}]")
        self.var_stock.set(row[4])
        
    def add_update_cart(self):
        if self.var_pid.get()=="":
            messagebox.showerror("Error","Please select product from the list",parent=self.root)
        elif self.var_qty.get()=="":
            messagebox.showerror("Error","Quantity is required",parent=self.root)
        elif int(self.var_qty.get())>int(self.var_stock.get()):
            messagebox.showerror("Error","Invalid Quantity",parent=self.root)
        else:
            #price_cal=int(self.var_qty.get())*float(self.var_price.get())
            #price_cal=float(price_cal)
            price_cal=self.var_price.get()
            cart_data=[self.var_pid.get(),self.var_pname.get(),price_cal,self.var_qty.get(),self.var_stock.get()]
            #---------- update cart --------------
            present="no"
            index_=0
            for row in self.cart_list:
                if self.var_pid.get()==row[0]:
                    present="yes"
                    break
                index_+=1
            if present=="yes":
                op=messagebox.askyesno("Confirm","Product already present\nDo you want to Update|Remove from the Cart List",parent=self.root)
                if op==True:
                    if self.var_qty.get()=="0":
                        self.cart_list.pop(index_)
                    else:
                        #self.cart_list[index_][2]=price_cal
                        self.cart_list[index_][3]=self.var_qty.get()
            else:
                self.cart_list.append(cart_data)
            self.show_cart()
            self.bill_update()

    def bill_update(self):
        """Calculate bill amount and apply discount from settings."""
        DB_PATH = resource_path('ims.db')
        con = sqlite3.connect(DB_PATH)

        cur = con.cursor()
        try:
            cur.execute("SELECT discount FROM settings WHERE id=1")
            row = cur.fetchone()
            if row:
                self.discount_rate = float(row[0])  # ✅ Fetch discount from settings
            else:
                self.discount_rate = 0  # Default to 1% if not found

        except Exception:
            self.discount_rate = 0  # Default in case of error

        con.close()

        # ✅ Calculate Discount
        self.bill_amnt = 0
        self.net_pay = 0
        for row in self.cart_list:
            self.bill_amnt += float(row[2]) * int(row[3])

        self.discount = (self.bill_amnt * self.discount_rate) / 100
        self.net_pay = self.bill_amnt - self.discount

        # ✅ Update Labels on UI
        self.lbl_amnt.config(text=f"Bill Amount\nRs. {str(self.bill_amnt)}")
        self.lbl_discount.config(text=f"Discount ({self.discount_rate}%)\nRs. {str(self.discount)}")
        self.lbl_net_pay.config(text=f"Net Pay\nRs. {str(self.net_pay)}")
        self.cartTitle.config(text=f"Cart \t Total Products: [{str(len(self.cart_list))}]")


    def show_cart(self):
        try:
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def generate_bill(self):
        if self.var_cname.get() == "" or self.var_contact.get() == "":
            messagebox.showerror("Error", "Customer Details are required", parent=self.root)
            return
        elif len(self.cart_list) == 0:
            messagebox.showerror("Error", "Please Add product to the Cart!", parent=self.root)
            return

        # ✅ **Correct invoice number generated once**
        self.invoice = int(time.strftime("%H%M%S")) + int(time.strftime("%d%m%Y"))

        DB_PATH = resource_path('ims.db')
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()

        try:
            # ✅ Insert into `sales`
            cur.execute("INSERT INTO sales (invoice_no, customer_name, customer_contact, total_amount, discount, net_pay, payment_method, emp_id, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                        (self.invoice, self.var_cname.get(), self.var_contact.get(), self.bill_amnt, self.discount, self.net_pay, 'Cash', self.emp_id, time.strftime("%d/%m/%Y")))

            # ✅ Insert into `selling_history`
            for row in self.cart_list:
                product_name = row[1]
                quantity = int(row[3])
                selling_price = float(row[2])
                total_amount = quantity * selling_price

                # ✅ Insert into `selling_history` with discount & net pay
                cur.execute("INSERT INTO selling_history (invoice_no, customer_name, product_name, quantity, selling_price, total_amount, discount, net_pay, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                            (self.invoice, self.var_cname.get(), product_name, quantity, selling_price, total_amount, self.discount, self.net_pay, time.strftime("%d/%m/%Y")))

                con.commit()
                self.log_activity(self.emp_id, "CREATE_BILL", self.invoice)  # ✅ Log the bill creation
                messagebox.showinfo("Success", f"Bill Generated: Invoice No {self.invoice}", parent=self.root)


        except Exception as e:
            messagebox.showerror("Error", f"Error saving sale: {str(e)}", parent=self.root)

        finally:
            con.close()

        # ✅ Generate Bill for Printing
        self.bill_top()
        self.bill_middle()
        self.bill_bottom()
        self.chk_print = 1






    def load_customers(self):
        """Fetch customer names and IDs from database and load them into the dropdown."""
        con = sqlite3.connect(resource_path("ims.db"))  # ✅ Uses the correct path
        cur = con.cursor()
        try:
            cur.execute("SELECT id, name FROM customer ORDER BY name ASC")
            customers = cur.fetchall()
            customer_list = ["Manual Entry"] + [f"{row[0]} - {row[1]}" for row in customers]  # Format: "ID - Name"
            self.customer_dropdown["values"] = customer_list
            self.customer_dropdown.current(0)  # Set default value
        except Exception as ex:
            messagebox.showerror("Error", f"Error fetching customers: {str(ex)}", parent=self.root)



    def fill_customer_details(self, event):
        """Auto-fill customer details when selected from dropdown, or allow manual entry."""
        selected_customer = self.var_customer.get()
        if selected_customer == "Manual Entry":
            self.var_cname.set("")
            self.var_contact.set("")
            return

        # Extract Customer ID from selected value
        customer_id = selected_customer.split(" - ")[0]

        con = sqlite3.connect(resource_path("ims.db"))  # ✅ Uses the correct path
        cur = con.cursor()
        try:
            cur.execute("SELECT name, contact FROM customer WHERE id=?", (customer_id,))
            customer = cur.fetchone()
            if customer:
                self.var_cname.set(customer[0])
                self.var_contact.set(customer[1])
            else:
                self.var_cname.set("")
                self.var_contact.set("")
                messagebox.showerror("Error", "Customer not found!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error fetching customer details: {str(ex)}", parent=self.root)




    def bill_top(self):
        """Fetch company details from settings and display them on the bill."""
        DB_PATH = resource_path('ims.db')
        con = sqlite3.connect(DB_PATH)

        cur = con.cursor()
        try:
            cur.execute("SELECT company_name, phone_number, address FROM settings WHERE id=1")
            settings = cur.fetchone()
            if settings:
                company_name = settings[0]
                phone_number = settings[1]
                address = settings[2]
            else:
                company_name = "Add Your Comp Name From Settings"
                phone_number = "Add Your Number From Settings"
                address = "Add Your City From Settings"
        except Exception:
            company_name = "Add Your Comp Name From Settings"
            phone_number = "Add Your Number From Settings"
            address = "Add Your City From Settings"

        # ✅ **FIXED: Use self.invoice from generate_bill()**
        bill_top_temp = f'''
    \t\t{company_name}
    \t {address}
    \t Phone No: {phone_number}
    {str("=" * 46)}
    Customer Name: {self.var_cname.get()}
    Ph. no. : {self.var_contact.get()}
    Bill No. {str(self.invoice)}\t\t\tDate: {str(time.strftime("%d/%m/%Y"))}
    {str("=" * 46)}
    Product Name\t\t\tQTY\tPrice
    {str("=" * 46)}
    '''
        self.txt_bill_area.delete('1.0', END)
        self.txt_bill_area.insert('1.0', bill_top_temp)



    def bill_bottom(self):
        """Display bill summary including the discount from settings."""
        bill_bottom_temp = f'''
{str("=" * 46)}
 Bill Amount\t\t\t\tRs. {self.bill_amnt}
 Discount ({self.discount_rate}%)\t\t\tRs. {self.discount}
 Net Pay\t\t\t\tRs. {self.net_pay}
{str("=" * 46)}\n
'''
        self.txt_bill_area.insert(END, bill_bottom_temp)


    def bill_middle(self):
        con = sqlite3.connect(resource_path("ims.db"))  # ✅ Uses the correct path
        cur=con.cursor()
        try:
            for row in self.cart_list:
                pid=row[0]
                name=row[1]
                qty=int(row[4])-int(row[3])
                if int(row[3])==int(row[4]):
                    status="Inactive"
                if int(row[3])!=int(row[4]):
                    status="Active"
                price=float(row[2])*int(row[3])
                price=str(price)
                self.txt_bill_area.insert(END,"\n "+name+"\t\t\t"+row[3]+"\tRs."+price)
                #------------- update qty in product table --------------
                cur.execute("update product set qty=?,status=? where pid=?",(
                    qty,
                    status,
                    pid
                ))
                con.commit()
            con.close()
            self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def clear_cart(self):
        self.var_pid.set("")
        self.var_pname.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.lbl_inStock.config(text=f"In Stock")
        self.var_stock.set("")

    def clear_all(self):
        del self.cart_list[:]
        self.clear_cart()
        self.show()
        self.show_cart()
        self.var_cname.set("")
        self.var_contact.set("")
        self.chk_print = 0 
        self.txt_bill_area.delete('1.0', END)
        self.cartTitle.config(text=f"Cart \t Total Products: [0]")
        self.var_search.set("")
        
    def update_date_time(self):
        time_=time.strftime("%I:%M:%S")
        date_=time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
        self.lbl_clock.after(200,self.update_date_time)

    def print_bill(self):
        if self.chk_print == 0:
            messagebox.showwarning("Print", "Please generate a bill before printing.", parent=self.root)
            return  # ✅ Don't clear data if no bill was generated!

        try:
            messagebox.showinfo("Print", "Saving bill...", parent=self.root)
            new_file = tempfile.mktemp('.txt')

            with open(new_file, 'w') as f:
                f.write(self.txt_bill_area.get('1.0', END))

            # Ensure the 'bill' folder exists
            BILL_DIR = os.path.join(BASE_DIR, "bill")
            if not os.path.exists(BILL_DIR):
                os.makedirs(BILL_DIR)

            # Save the bill in the bill directory
            bill_file_path = os.path.join(BILL_DIR, f"{str(self.invoice)}.txt")
            with open(bill_file_path, 'w') as fp:
                fp.write(self.txt_bill_area.get('1.0', END))

            # ✅ Move `clear_all()` to the end, after printing
            self.clear_all()  

            # ✅ Check if a printer is available before printing
            printer_found = False

            if platform.system() == "Windows":
                try:
                    subprocess.run(["wmic", "printer", "get", "name"], capture_output=True, text=True)
                    printer_found = True
                    os.startfile(new_file, 'print')
                except Exception:
                    pass

            elif platform.system() == "Darwin":  # macOS
                try:
                    result = subprocess.run(["lpstat", "-p"], capture_output=True, text=True)
                    if "printer" in result.stdout:
                        printer_found = True
                        subprocess.run(["lpr", new_file])
                except Exception:
                    pass

            elif platform.system() == "Linux":
                try:
                    result = subprocess.run(["lpstat", "-p"], capture_output=True, text=True)
                    if "printer" in result.stdout:
                        printer_found = True
                        subprocess.run(["lp", new_file])
                except Exception:
                    pass

            if not printer_found:
                messagebox.showwarning("Print Error", "Printer is not connected. Bill is saved but not printed.", parent=self.root)

        except Exception as e:
            messagebox.showerror("Error", f"Printing error: {str(e)}", parent=self.root)



if __name__=="__main__":
    root=Tk()
    obj=billClass(root, emp_id="TEST_USER")
    root.mainloop()