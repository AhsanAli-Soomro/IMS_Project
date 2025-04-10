from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
import os,sys  # ✅ Import OS for handling paths
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller."""
    try:
        base_path = sys._MEIPASS  # When running from PyInstaller
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))  # When running normally
    return os.path.join(base_path, relative_path)


DB_PATH = resource_path('ims.db')  # ✅ Ensures correct path in .exe
con = sqlite3.connect(DB_PATH)
class categoryClass(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg="white")
        self.pack(fill=BOTH, expand=True)  # ✅ Ensures full screen scaling

        # ✅ Get the base directory path
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        image1_path = os.path.join(BASE_DIR, "images", "cat.jpg")
        image2_path = os.path.join(BASE_DIR, "images", "category.jpg")

        #------------ Variables -------------
        self.var_cat_id = StringVar()
        self.var_name = StringVar()

        #--------------- Title ---------------------
        Label(self, text="Manage Product Category", font=("Arial", 20, "bold"), 
            bg="#0f4d7d", fg="white", padx=20, pady=10).pack(fill=X, anchor=CENTER)

        #--------------- Main Frame ---------------------
        main_frame = Frame(self, bg="white")
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        #--------------- Left Form Frame ---------------------
        form_frame = Frame(main_frame, bg="white", bd=2, relief=RIDGE)
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        Label(form_frame, text="Enter Category Name", font=("goudy old style", 20), bg="white").grid(row=0, column=0, padx=10, pady=10, sticky=W)
        Entry(form_frame, textvariable=self.var_name, bg="lightyellow", font=("goudy old style", 15)).grid(row=0, column=1, padx=10, pady=10, ipadx=50)

        # ------------ Category Buttons ---------------------
        btn_frame = Frame(form_frame, bg="white")
        btn_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")  # ✅ Sticky ensures it stretches

        buttons = [
            ("ADD", self.add, "#4caf50"),
            ("Delete", self.delete, "red"),
        ]

        for i, (text, cmd, color) in enumerate(buttons):
            btn = Button(btn_frame, text=text, command=cmd, font=("goudy old style", 15),
                         bg=color, fg="white", cursor="hand2")
            btn.grid(row=0, column=i, padx=10, pady=10, sticky="ew")  # ✅ Buttons stretch horizontally
            btn_frame.grid_columnconfigure(i, weight=1)  # ✅ Ensures equal width for buttons

        # ------------ Category Details Table ---------------------
        table_frame = Frame(main_frame, bg="white", bd=3, relief=RIDGE)
        table_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")  # ✅ Expands dynamically

        main_frame.grid_columnconfigure(1, weight=2)  # ✅ Allows table frame to expand more
        main_frame.grid_rowconfigure(0, weight=1)

        scrolly = Scrollbar(table_frame, orient=VERTICAL)
        scrollx = Scrollbar(table_frame, orient=HORIZONTAL)

        self.CategoryTable = ttk.Treeview(
            table_frame, columns=("cid", "name"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set
        )
        
        # Scrollbar Configuration
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.CategoryTable.xview)
        scrolly.config(command=self.CategoryTable.yview)

        # Table Headings
        self.CategoryTable.heading("cid", text="Category ID")
        self.CategoryTable.heading("name", text="Name")
        self.CategoryTable["show"] = "headings"

        # Table Column Widths (Auto-Adjusting)
        self.CategoryTable.column("cid", width=100, minwidth=80, anchor=CENTER)
        self.CategoryTable.column("name", width=250, minwidth=150, anchor=W)

        # Table Packing
        self.CategoryTable.pack(fill=BOTH, expand=True)
        self.CategoryTable.bind("<ButtonRelease-1>", self.get_data)
        self.show()


        #----------------- Images ---------------------
        image_frame = Frame(self, bg="white")
        image_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        try:
            if os.path.exists(image1_path):
                self.im1 = Image.open(image1_path)
                self.im1 = self.im1.resize((400, 200))  # ✅ Adjusted for responsiveness
                self.im1 = ImageTk.PhotoImage(self.im1)
                self.lbl_im1 = Label(image_frame, image=self.im1, bd=2, relief=RAISED)
                self.lbl_im1.grid(row=0, column=0, padx=10, pady=10)

            if os.path.exists(image2_path):
                self.im2 = Image.open(image2_path)
                self.im2 = self.im2.resize((400, 200))  # ✅ Adjusted for responsiveness
                self.im2 = ImageTk.PhotoImage(self.im2)
                self.lbl_im2 = Label(image_frame, image=self.im2, bd=2, relief=RAISED)
                self.lbl_im2.grid(row=0, column=1, padx=10, pady=10)

        except Exception as e:
            print(f"Error loading images: {e}")



    # ----------------- Database Methods -----------------
    def add(self):
        con = sqlite3.connect(resource_path("ims.db"))  # ✅ Uses the correct path
        cur = con.cursor()
        try:
            if self.var_name.get() == "":
                messagebox.showerror("Error", "Category Name must be required", parent=self)
            else:
                cur.execute("Select * from category where name=?", (self.var_name.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Category already present", parent=self)
                else:
                    cur.execute("insert into category(name) values(?)", (self.var_name.get(),))
                    con.commit()
                    messagebox.showinfo("Success", "Category Added Successfully", parent=self)
                    self.clear()
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")

    def show(self):
        con = sqlite3.connect(resource_path("ims.db"))  # ✅ Uses the correct path
        cur = con.cursor()
        try:
            cur.execute("select * from category")
            rows = cur.fetchall()
            self.CategoryTable.delete(*self.CategoryTable.get_children())
            for row in rows:
                self.CategoryTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")

    def clear(self):
        self.var_name.set("")
        self.show()

    def get_data(self, ev):
        f = self.CategoryTable.focus()
        content = (self.CategoryTable.item(f))
        row = content['values']
        if row:
            self.var_cat_id.set(row[0])
            self.var_name.set(row[1])

    def delete(self):
        con = sqlite3.connect(resource_path("ims.db"))  # ✅ Uses the correct path
        cur = con.cursor()
        try:
            if self.var_cat_id.get() == "":
                messagebox.showerror("Error", "Category name must be required", parent=self)
            else:
                cur.execute("Select * from category where cid=?", (self.var_cat_id.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Category Name", parent=self)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self)
                    if op:
                        cur.execute("delete from category where cid=?", (self.var_cat_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Category Deleted Successfully", parent=self)
                        self.clear()
                        self.var_cat_id.set("")
                        self.var_name.set("")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")
