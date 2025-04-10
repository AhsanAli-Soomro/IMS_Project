from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import sqlite3
import os,sys
import datetime
import importlib  # To handle imports dynamically

# Get the base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__)) 
    return os.path.join(base_path, relative_path)


# ✅ Get the database path
DB_PATH = resource_path('ims.db')
con = sqlite3.connect(DB_PATH)



# Image Paths
logo_path = os.path.join(BASE_DIR, "logo", "company_logo.png")  
image_path = os.path.join(BASE_DIR, "images", "logo1.png")  
class LoginSystem:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x600+350+100")
        self.root.title("Login | Inventory Management System")
        self.root.resizable(False, False)
        self.root.config(bg="white")
 
        self.var_emp_id = StringVar()
        self.var_password = StringVar()

        # ====== Center Login Frame ======
        login_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        login_frame.place(relx=0.5, rely=0.5, anchor=CENTER, width=400, height=420)

        # ====== Title ======
        self.icon_title = PhotoImage(file=image_path)
        title = Label(self.root, text="Inventory Management System", image=self.icon_title,
                      compound=LEFT, font=("times new roman", 25, "bold"), bg="#010c48",
                      fg="white", anchor="w", padx=20)
        title.place(x=0, y=0, relwidth=1, height=70)

        # ====== Company Logo at Top ======
        self.logo_img = Image.open(logo_path)
        self.logo_img = self.logo_img.resize((100, 100), Image.LANCZOS)
        self.logo_img = ImageTk.PhotoImage(self.logo_img)
        Label(login_frame, image=self.logo_img, bg="white").pack(pady=10)

        Label(login_frame, text="Login", font=("Arial", 22, "bold"), bg="white", fg="#010c48").pack()

        # ====== Employee ID Input ======
        Label(login_frame, text="Employee ID:", font=("Arial", 14), bg="white").pack(pady=(20, 0), anchor="w", padx=30)
        Entry(login_frame, textvariable=self.var_emp_id, font=("Arial", 14), bg="#f7f7f7").pack(pady=5, padx=30, fill="x")

        # ====== Password Input ======
        Label(login_frame, text="Password:", font=("Arial", 14), bg="white").pack(pady=(10, 0), anchor="w", padx=30)
        Entry(login_frame, textvariable=self.var_password, font=("Arial", 14), bg="#f7f7f7", show="*").pack(pady=5, padx=30, fill="x")

        # ====== Login Button ======
        btn_login = Label(login_frame, text="Login", cursor="hand2",
                        font=("Arial", 14, "bold"), bg="#009688", fg="white",
                        relief=FLAT, padx=10, pady=5)

        # ✅ Add Click Event
        btn_login.bind("<Button-1>", lambda e: self.login())  # Simulate button click

        # ✅ Add Hover Effect
        btn_login.bind("<Enter>", lambda e: btn_login.config(bg="#00796B"))  # Darker shade on hover
        btn_login.bind("<Leave>", lambda e: btn_login.config(bg="#009688"))  # Restore original color

        btn_login.pack(pady=20, padx=30, fill="x")


    def login(self):
        emp_id = self.var_emp_id.get().strip()
        password = self.var_password.get().strip()

        if emp_id == "" or password == "":
            messagebox.showerror("Error", "All fields are required!", parent=self.root)
            return

        # ✅ Print debug info
        print(f"Connecting to database at: {DB_PATH}")

        # ✅ Define con before the try block
        con = None

        try:
            # ✅ Now connect to the database
            con = sqlite3.connect(DB_PATH)
            cur = con.cursor()
            cur.execute("SELECT utype FROM employee WHERE eid=? AND pass=?", (emp_id, password))
            user = cur.fetchone()

            if user:
                user_type = user[0]

                # ✅ Log successful login
                self.log_activity(emp_id, "LOGIN")

                self.root.destroy()  # ✅ Close login window after successful login

                if user_type == "Admin":
                    dashboard_module = importlib.import_module("dashboard")
                    root = Tk()
                    dashboard_module.IMS(root, emp_id)  # ✅ Pass emp_id to Dashboard
                    root.mainloop()

                elif user_type == "Employee":
                    billing_module = importlib.import_module("billing")  # ✅ Ensure it's imported
                    root = Tk()
                    billing_module.billClass(root, emp_id)  # ✅ Pass emp_id to Billing
                    root.mainloop()
            else:
                self.log_activity(emp_id, "FAILED_ATTEMPT")  # ✅ Log failed login attempts
                messagebox.showerror("Error", "Invalid Employee ID or Password", parent=self.root)

        except sqlite3.Error as ex:
            print(f"Database Error: {str(ex)}")  # ✅ Print error in Terminal
            messagebox.showerror("Database Error", f"Error due to: {str(ex)}", parent=self.root)

        finally:
            if con:  # ✅ Ensure connection is only closed if it was opened
                con.close()


    def log_activity(self, emp_id, action):
        """Log user activities (Login, Logout, Failed Attempts) with timestamps"""
        
        # ✅ Get the correct current timestamp
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")  # Format: YYYY-MM-DD HH:MM:SS

        # ✅ Debugging: Print the timestamp to confirm it's correct
        print(f"Logging action: {action} for Employee ID: {emp_id} at {timestamp}")

        try:
            con = sqlite3.connect(DB_PATH)
            cur = con.cursor()

            # ✅ Store timestamp with each log entry
            cur.execute("INSERT INTO logs (emp_id, action, timestamp) VALUES (?, ?, ?)", (emp_id, action, timestamp))
            con.commit()
        except Exception as ex:
            print(f"Error logging action: {str(ex)}")
        finally:
            con.close()

if __name__ == "__main__":
    root = Tk()
    LoginSystem(root)
    root.mainloop()
