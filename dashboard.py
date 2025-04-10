from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import time
import sqlite3
import os
from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass
from customer import CustomerClass
from logs import LogsPage
from settings import SettingsClass
from billing import billClass
from reports import ReportsPage
from selling_history import SellingHistory
from SupplierProductPurchaseHistory import SupplierPurchaseHistory
import importlib

# Get base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Paths for images
image_path = os.path.join(BASE_DIR, "logo", "company_logo.png")
menu_image_path = os.path.join(BASE_DIR, "images", "menu_im.png")
side_image_path = os.path.join(BASE_DIR, "images", "side.png")

# Ensure the 'bill' folder exists
BILL_DIR = os.path.join(BASE_DIR, "bill")
if not os.path.exists(BILL_DIR):
    os.makedirs(BILL_DIR)


class IMS:
    def __init__(self, root, emp_id):
        self.root = root
        self.emp_id = emp_id
        self.root.geometry("1350x900+110+80")
        self.company_name = self.get_company_name()
        self.root.title(f"{self.company_name} | Inventory Management System")
        self.root.resizable(True, True)
        self.root.config(bg="white")

        # Enable fullscreen toggle
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)

        # ---------- Title Bar ----------
        image = Image.open(image_path)
        resized_image = image.resize((50, 50), Image.LANCZOS)
        self.icon_title = ImageTk.PhotoImage(resized_image)

        # Set Dynamic Title
        title_text = f"{self.company_name} Inventory Management System"
        self.title_label = Label(self.root, text=title_text, image=self.icon_title,
                                 compound=LEFT, font=("times new roman", 36, "bold"),
                                 bg="#010c48", fg="white", anchor="w", padx=20)
        self.title_label.place(x=0, y=0, relwidth=1, height=70)

        # Logout button
        btn_logout = Label(self.root, text="Logout", cursor="hand2",
                        font=("times new roman", 15, "bold"), bg="yellow", fg="black",
                        relief=RAISED, padx=10, pady=5)

        # ✅ Add Click Event
        btn_logout.bind("<Button-1>", lambda e: self.logout())

        # ✅ Add Hover Effect
        btn_logout.bind("<Enter>", lambda e: btn_logout.config(bg="#FFD700")) 
        btn_logout.bind("<Leave>", lambda e: btn_logout.config(bg="yellow")) 

        btn_logout.place(relx=0.85, y=10, height=50, width=150)


        # ---------- Sidebar Menu ----------
        self.MenuLogo = Image.open(menu_image_path).resize((200, 200))  # Adjusted from 200 to 280
        self.MenuLogo = ImageTk.PhotoImage(self.MenuLogo)


        # ---------- Sidebar Menu (Fixed Size) ----------
        LeftMenu = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        LeftMenu.place(x=0, y=102, width=200, relheight=0.90)  # Increased from 200 to 320




        lbl_menuLogo = Label(LeftMenu, image=self.MenuLogo)
        lbl_menuLogo.pack(side=TOP, fill=X)

        lbl_menu = Label(LeftMenu, text="Menu", font=("times new roman", 20), bg="#009688")
        lbl_menu.pack(side=TOP, fill=X)

        self.icon_side = PhotoImage(file=side_image_path)
        self.icon_side = self.icon_side.subsample(2, 2)

        menu_buttons = [
            ("Dashboard", self.show_dashboard), 
            ("Employee", self.employee),
            ("Supplier", self.supplier),
            ("Customer", self.customer),
            ("Category", self.category),
            ("Products", self.product),
            ("Sales", self.sales),
            ("Reports", self.reports),
            ("Selling History", self.selling_history),
            ("Purchase History", self.supplier_product_purchase_history),
            ("Logs", self.logs),
            ("Settings", self.settings),
            ("Exit", self.exit_app),
        ]

        # Create a dictionary to store menu buttons
        self.menu_buttons_dict = {}

        for text, command in menu_buttons:
            btn = Button(LeftMenu, text=text, command=lambda cmd=command, btn_text=text: self.set_active_button(btn_text, cmd),
                        image=self.icon_side, compound=LEFT,
                        padx=5, anchor="w", font=("times new roman", 15, "bold"),
                        bg="white", bd=3, cursor="hand2", justify=LEFT)

            btn.pack(side=TOP, fill=X, padx=5, pady=3)
            self.menu_buttons_dict[text] = btn  # Store button reference





        # ---------- Dashboard Frame (FULL WINDOW) ----------
        self.dashboard_frame = Frame(self.root, bg="white")
        self.dashboard_frame.place(x=200, y=50, relwidth=0.85, relheight=0.90)

        # ---------- Bill Header ----------
        self.btn_billing = Label(self.dashboard_frame, text="Billing", cursor="hand2",
                            font=("times new roman", 15, "bold"), bg="#71db5e", fg="black",
                            relief=RAISED, padx=10, pady=5)

        self.btn_billing.bind("<Button-1>", lambda e: self.billing())
        self.btn_billing.bind("<Leave>", lambda e: self.btn_billing.config(bg="#71db5e"))
        self.btn_billing.bind("<Enter>", lambda e: self.btn_billing.config(bg="#53a145"))

        # ---------- Dashboard Stats ----------
        self.lbl_employee = Label(self.dashboard_frame, text="Total Employee\n{ 0 }", bd=5, relief=RIDGE,
                                bg="#33bbf9", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_employee.place(relx=0.12, rely=0.15, relwidth=0.2, relheight=0.15)

        self.lbl_supplier = Label(self.dashboard_frame, text="Total Supplier\n{ 0 }", bd=5, relief=RIDGE,
                                bg="#ff5722", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_supplier.place(relx=0.34, rely=0.15, relwidth=0.2, relheight=0.15)

        self.lbl_category = Label(self.dashboard_frame, text="Total Category\n{ 0 }", bd=5, relief=RIDGE,
                                bg="#009688", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_category.place(relx=0.56, rely=0.15, relwidth=0.2, relheight=0.15)

        self.lbl_customer = Label(self.dashboard_frame, text="Total Customers\n{ 0 }", bd=5, relief=RIDGE,
                                bg="#8e44ad", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_customer.place(relx=0.78, rely=0.15, relwidth=0.2, relheight=0.15)

        self.lbl_product = Label(self.dashboard_frame, text="Total Product\n{ 0 }", bd=5, relief=RIDGE,
                                bg="#607d8b", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_product.place(relx=0.12, rely=0.40, relwidth=0.2, relheight=0.15)

        self.lbl_sales = Label(self.dashboard_frame, text="Total Sales\n{ 0 }", bd=5, relief=RIDGE,
                            bg="#ffc107", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_sales.place(relx=0.34, rely=0.40, relwidth=0.2, relheight=0.15)

        # ✅ Store all stat labels in a list (IMPORTANT)
        self.stat_widgets = [
            self.lbl_employee,
            self.lbl_supplier,
            self.lbl_category,
            self.lbl_customer,
            self.lbl_product,
            self.lbl_sales
            
        ]

        # ---------- Content Frame (FULL WINDOW) ----------
        self.content_frame = Frame(self.root, bg="white")
        self.content_frame.place(x=200, y=102, relwidth=0.85, relheight=0.85) 


        # Initially show dashboard
        self.show_dashboard()
        self.update_content()
        

    # ---------------------- Functions ----------------------
    def show_dashboard(self):
        """Show the dashboard and hide the content frame."""
        self.content_frame.place_forget()  # Hide content frame
        self.dashboard_frame.place(x=200, y=102, relwidth=0.85, relheight=0.85) 
        self.btn_billing.place(relx=0.85, y=0.015, height=50, width=150)
        self.update_content()  # Ensure data refresh



    def show_frame(self, page_class):
        """Show a new page and hide the dashboard."""
        self.dashboard_frame.place_forget()  # Hide dashboard
        self.btn_billing.place_forget()
        self.content_frame.place(x=200, y=102, relwidth=0.85, relheight=0.85)  # Expand content frame

        for widget in self.content_frame.winfo_children():
            widget.destroy()  # Clear old content

        page = page_class(self.content_frame)
        page.pack(fill=BOTH, expand=True)  # ✅ Ensure Full Frame Visibility

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
        
    def update_dashboard_title(self):
        """Update the dashboard title when settings change."""
        self.company_name = self.get_company_name()
        title_text = f"{self.company_name} Inventory Management System"
        self.title_label.config(text=title_text)

    def set_active_button(self, active_text, command):
        """ Change the active button's background color """
        
        for text, btn in self.menu_buttons_dict.items():
            if text == active_text:
                btn.config(bg="#4CAF50", fg="red")  # Active button color (Green)
            else:
                btn.config(bg="white", fg="black")  # Reset others to default
        
        command()  # Execute the original button function



    # ✅ Call update function periodically to check for updates
    def auto_update_title(self):
        self.update_dashboard_title()
        self.root.after(5000, self.auto_update_title)
        
    # Navigation Functions
    def employee(self):
        self.show_frame(employeeClass)

    def supplier(self):
        self.show_frame(supplierClass)

    def customer(self):
        self.show_frame(CustomerClass)

    def category(self):
        self.show_frame(categoryClass)

    def product(self):
        self.show_frame(productClass)

    def sales(self):
        self.show_frame(salesClass)

    def logs(self):
        self.show_frame(LogsPage)

    def reports(self):
        self.show_frame(ReportsPage)
    
    def selling_history(self):
        self.show_frame(SellingHistory)

    def supplier_product_purchase_history(self):
        self.show_frame(SupplierPurchaseHistory)
    
    def settings(self):
        self.show_frame(SettingsClass)
    def exit_app(self):
        self.root.destroy()


    def toggle_fullscreen(self, event=None):
        """Toggle full-screen mode"""
        self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen"))

    def exit_fullscreen(self, event=None):
        """Exit full-screen mode"""
        self.root.attributes("-fullscreen", False)
    def logout(self):
        """Log out and go back to the login screen."""
        self.log_activity(self.emp_id, "LOGOUT")  # ✅ Log the logout action
        self.root.destroy()  # Close the current Dashboard window
        login_module = importlib.import_module("login")  # Open Login Page
        root = Tk()
        login_module.LoginSystem(root)
        root.mainloop()

    def billing(self):
        """Open the billing window with the current employee ID."""
        self.log_activity(self.emp_id, "OPEN_BILLING")  # ✅ Log before anything else
        login_module = importlib.import_module("billing")
        self.root.destroy()
        root = Tk()
        login_module.billClass(root, emp_id=self.emp_id)
        root.mainloop()



    
    def log_activity(self, emp_id, action, invoice_no=None):
        con = sqlite3.connect(os.path.join(BASE_DIR, 'ims.db'))
        cur = con.cursor()
        cur.execute("INSERT INTO logs (emp_id, action, invoice_no) VALUES (?, ?, ?)",
                    (emp_id, action, invoice_no))
        con.commit()
        con.close()


    def log_action(emp_id, action):
        """Insert an action into the logs table."""
        con = sqlite3.connect(database="ims.db")
        cur = con.cursor()
        try:
            cur.execute("INSERT INTO logs (emp_id, action) VALUES (?, ?)", (emp_id, action))
            con.commit()
        except Exception as ex:
            print(f"Error logging action: {str(ex)}")


    def update_content(self):
        """Fetch data from the database and update dashboard stats dynamically"""
        try:
            db_path = os.path.join(BASE_DIR, 'ims.db')
            print(f"🔍 Using database path: {db_path}")  # ✅ Debug print

            con = sqlite3.connect(db_path)
            cur = con.cursor()

            # ✅ Print all table names (Debugging)
            cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cur.fetchall()
            print(f"🛠 Tables found in DB: {tables}")

            # Fetch total employee count
            cur.execute("SELECT COUNT(*) FROM employee")
            total_employees = cur.fetchone()[0]
            print(f"👨‍💼 Total Employees: {total_employees}")
            self.stat_widgets[0].config(text=f"Total Employee\n{total_employees}")

            # Fetch total supplier count
            cur.execute("SELECT COUNT(*) FROM supplier")
            total_suppliers = cur.fetchone()[0]
            print(f"🏢 Total Suppliers: {total_suppliers}")
            self.stat_widgets[1].config(text=f"Total Supplier\n{total_suppliers}")

            # Fetch total category count
            cur.execute("SELECT COUNT(*) FROM category")
            total_categories = cur.fetchone()[0]
            print(f"📦 Total Categories: {total_categories}")
            self.stat_widgets[2].config(text=f"Total Category\n{total_categories}")

            # Fetch total customer count
            cur.execute("SELECT COUNT(*) FROM customer")
            total_customers = cur.fetchone()[0]
            print(f"👥 Total Customers: {total_customers}")
            self.stat_widgets[3].config(text=f"Total Customers\n{total_customers}")

            # Fetch total product count
            cur.execute("SELECT COUNT(*) FROM product")
            total_products = cur.fetchone()[0]
            print(f"🛒 Total Products: {total_products}")
            self.stat_widgets[4].config(text=f"Total Product\n{total_products}")

            # Fetch total sales count (Check if folder exists)
            if not os.path.exists(BILL_DIR):
                print("⚠️ Warning: 'bill' directory does not exist!")
                total_sales = 0
            else:
                total_sales = len(os.listdir(BILL_DIR))
            print(f"💰 Total Sales: {total_sales}")
            self.stat_widgets[5].config(text=f"Total Sales\n{total_sales}")

            con.close()

            # ✅ Auto-refresh dashboard every 5 seconds
            self.root.after(5000, self.update_content)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
            print(f"❌ SQL Error: {str(ex)}")  # ✅ Debug print




if __name__ == "__main__":
    root = Tk()
    obj = IMS(root)
    root.mainloop()
