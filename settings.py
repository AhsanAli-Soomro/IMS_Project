import os
import shutil
import sqlite3
import datetime
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'ims.db')
BACKUP_DIR = os.path.join(BASE_DIR, 'backup')
LOGO_DIR = os.path.join(BASE_DIR, 'logo')

# Ensure directories exist
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

if not os.path.exists(LOGO_DIR):
    os.makedirs(LOGO_DIR)

class SettingsClass(Frame):

    def __init__(self, parent):
        super().__init__(parent)  # ✅ Call Frame's constructor
        self.configure(bg="white")  # ✅ Set background color
        # Variables
        self.var_company_name = StringVar()
        self.var_phone_number = StringVar()
        self.var_address = StringVar()
        self.var_discount = StringVar()
        self.logo_path = StringVar()

        # Title
        title = Label(self, text="Company Settings & Backup", font=("Arial", 20, "bold"), 
                      bg="#0f4d7d", fg="white", bd=10, pady=10, relief=RIDGE)
        title.pack(side=TOP, fill=X)

        # Labels & Input Fields
        lbl_company = Label(self, text="Company Name", font=("goudy old style", 15), bg="white").place(x=50, y=80)
        txt_company = Entry(self, textvariable=self.var_company_name, font=("goudy old style", 15), bg="lightyellow")
        txt_company.place(x=220, y=80, width=300)

        lbl_phone = Label(self, text="Phone Number", font=("goudy old style", 15), bg="white").place(x=50, y=130)
        txt_phone = Entry(self, textvariable=self.var_phone_number, font=("goudy old style", 15), bg="lightyellow")
        txt_phone.place(x=220, y=130, width=300)

        lbl_address = Label(self, text="Address", font=("goudy old style", 15), bg="white").place(x=50, y=180)
        self.txt_address = Text(self, font=("goudy old style", 15), bg="lightyellow")
        self.txt_address.place(x=220, y=180, width=300, height=60)

        lbl_discount = Label(self, text="Discount (%)", font=("goudy old style", 15), bg="white").place(x=50, y=260)
        txt_discount = Entry(self, textvariable=self.var_discount, font=("goudy old style", 15), bg="lightyellow")
        txt_discount.place(x=220, y=260, width=100)

        # Logo Upload Section
        lbl_logo = Label(self, text="Company Logo", font=("goudy old style", 15), bg="white").place(x=50, y=310)
        self.logo_label = Label(self, bg="white", bd=2, relief=SOLID)
        self.logo_label.place(x=220, y=310, width=100, height=100)

        btn_upload_logo = Button(self, text="Upload Logo", command=self.upload_logo, font=("Arial", 12), bg="#FFC107", fg="black")
        btn_upload_logo.place(x=340, y=340, width=120, height=35)

        # Buttons
        btn_save = Button(self, text="Save", command=self.update_settings, font=("goudy old style", 15), bg="#2196f3", fg="white", cursor="hand2")
        btn_save.place(x=220, y=440, width=100, height=35)

        btn_close = Button(self, text="Close", command=self.destroy, font=("goudy old style", 15), bg="red", fg="white", cursor="hand2")
        btn_close.place(x=340, y=440, width=100, height=35)

        # Backup & Restore Section
        Label(self, text="Backup & Restore", font=("Arial", 16, "bold"), bg="white").place(x=50, y=480)

        btn_backup = Button(self, text="Backup Now", command=self.backup_database, font=("Arial", 12), bg="#2196F3", fg="white")
        btn_backup.place(x=50, y=540, width=200, height=35)

        btn_restore = Button(self, text="Restore Backup", command=self.restore_database, font=("Arial", 12), bg="#4CAF50", fg="white")
        btn_restore.place(x=260, y=540, width=200, height=35)

        self.last_backup_label = Label(self, text=f"Last Backup: {self.get_last_backup_time()}", font=("Arial", 10), bg="white")
        self.last_backup_label.place(x=50, y=590)

        self.load_settings()

    def upload_logo(self):
        """Upload and display the company logo."""
        try:
            file_path = filedialog.askopenfilename(
                title="Select Logo",
                filetypes=[("Image Files", ("*.png", "*.jpg", "*.jpeg", "*.gif"))]
            )

            if not file_path:  # If the user cancels, stop execution
                messagebox.showwarning("Warning", "No file selected!", parent=self)
                return

            # Ensure file exists before copying
            if not os.path.exists(file_path):
                messagebox.showerror("Error", "Selected file does not exist!", parent=self)
                return

            # Define the logo storage location
            logo_filename = os.path.join(LOGO_DIR, "company_logo.png")

            # Copy file to the designated logo directory
            shutil.copy2(file_path, logo_filename)

            # Store the new logo path
            self.logo_path.set(logo_filename)

            # Display the new logo
            self.display_logo(logo_filename)

        except shutil.Error as e:
            messagebox.showerror("Error", f"Failed to copy logo: {str(e)}", parent=self)
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}", parent=self)



    def display_logo(self, path):
        """Display the uploaded logo."""
        try:
            if not os.path.exists(path):
                messagebox.showerror("Error", "Logo file not found!", parent=self)
                return

            print(f"Loading image from: {path}")  # DEBUGGING LINE

            img = Image.open(path)
            img = img.resize((100, 100), Image.LANCZOS)  # Ensure compatibility
            img = ImageTk.PhotoImage(img)

            self.logo_label.config(image=img)
            self.logo_label.image = img  # Keep a reference to avoid garbage collection
            print("Image displayed successfully!")  # DEBUGGING LINE

        except Exception as e:
            messagebox.showerror("Error", f"Failed to display logo: {str(e)}", parent=self)
            print(f"Image loading error: {e}")  # DEBUGGING LINE



    def load_settings(self):
        """Load current settings from the database."""
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        try:
            cur.execute("SELECT company_name, phone_number, address, discount FROM settings WHERE id=1")
            row = cur.fetchone()
            if row:
                self.var_company_name.set(row[0])
                self.var_phone_number.set(row[1])
                self.txt_address.insert("1.0", row[2])
                self.var_discount.set(row[3])

            logo_path = os.path.join(LOGO_DIR, "company_logo.png")
            if os.path.exists(logo_path):
                self.logo_path.set(logo_path)
                self.display_logo(logo_path)

        except Exception as ex:
            messagebox.showerror("Error", f"Error fetching settings: {str(ex)}", parent=self)

    def update_settings(self):
        """Update company settings in the database."""
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        try:
            cur.execute("UPDATE settings SET company_name=?, phone_number=?, address=?, discount=? WHERE id=1", (
                self.var_company_name.get(),
                self.var_phone_number.get(),
                self.txt_address.get("1.0", END).strip(),
                self.var_discount.get()
            ))
            con.commit()
            messagebox.showinfo("Success", "Settings updated successfully", parent=self)
        except Exception as ex:
            messagebox.showerror("Error", f"Error updating settings: {str(ex)}", parent=self)


    def backup_database(self):
        """Creates a backup of the current database."""
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(BACKUP_DIR, f"ims_backup_{timestamp}.db")

            shutil.copy2(DB_PATH, backup_file)  # Copy database to backup folder

            messagebox.showinfo("Success", f"Database backup saved successfully!\nLocation: {backup_file}")
            self.last_backup_label.config(text=f"Last Backup: {self.get_last_backup_time()}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to backup database: {str(e)}")

    def restore_database(self):
        """Restores database from a selected backup file."""
        try:
            file_path = filedialog.askopenfilename(initialdir=BACKUP_DIR, title="Select Backup File",
                                                   filetypes=(("Database Files", "*.db"), ("All Files", "*.*")))
            if not file_path:
                return  # User canceled selection

            shutil.copy2(file_path, DB_PATH)  # Replace current database with backup

            messagebox.showinfo("Success", "Database restored successfully! Restart the application.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to restore database: {str(e)}")

    def get_last_backup_time(self):
        """Gets the last backup time from the latest backup file."""
        try:
            backups = sorted([f for f in os.listdir(BACKUP_DIR) if f.startswith("ims_backup_")], reverse=True)
            if backups:
                last_backup = backups[0].replace("ims_backup_", "").replace(".db", "")
                return datetime.datetime.strptime(last_backup, "%Y%m%d_%H%M%S").strftime("%d-%m-%Y %H:%M:%S")
            return "No backups available"
        except Exception as e:
            return "Error fetching backup time"

