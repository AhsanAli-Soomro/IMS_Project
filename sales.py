from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
import os

# Get base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cat2 = os.path.join(BASE_DIR, "images", "cat2.jpg")

# Ensure 'bill' folder exists
BILL_DIR = os.path.join(BASE_DIR, "bill")
if not os.path.exists(BILL_DIR):
    os.makedirs(BILL_DIR)

class salesClass(Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg="white")

        self.blll_list = []
        self.var_invoice = StringVar()

        # ✅ Full-Width Title
        lbl_title = Label(self, text="View Customer Bills", font=("Arial", 20, "bold"),
                          bg="#0f4d7d", fg="white", bd=10, relief=RIDGE)
        lbl_title.pack(side=TOP, fill=X, padx=10, pady=10, ipady=10)

        # ✅ Search Frame
        search_frame = Frame(self, bg="white")
        search_frame.pack(fill=X, padx=20, pady=10)

        lbl_invoice = Label(search_frame, text="Invoice No:", font=("times new roman", 15), bg="white")
        lbl_invoice.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        txt_invoice = Entry(search_frame, textvariable=self.var_invoice, font=("times new roman", 15), bg="lightyellow")
        txt_invoice.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        btn_search = Button(search_frame, text="Search", command=self.search, font=("times new roman", 15, "bold"),
                            bg="#2196f3" , cursor="hand2")
        btn_search.grid(row=0, column=2, padx=10, pady=5)

        btn_clear = Button(search_frame, text="Clear", command=self.clear, font=("times new roman", 15, "bold"),
                           bg="lightgray", cursor="hand2")
        btn_clear.grid(row=0, column=3, padx=10, pady=5)

        # ✅ Main Content Frame (Sales List & Bill Display)
        content_frame = Frame(self, bg="white")
        content_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

        # ✅ Sales List (Left Side)
        sales_Frame = Frame(content_frame, bd=3, relief=RIDGE)
        sales_Frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsw")

        lbl_sales = Label(sales_Frame, text="Sales List", font=("goudy old style", 18, "bold"), bg="lightgray")
        lbl_sales.pack(side=TOP, fill=X)

        scrolly = Scrollbar(sales_Frame, orient=VERTICAL)
        self.Sales_List = Listbox(sales_Frame, font=("goudy old style", 15), bg="white", yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT, fill=Y)
        scrolly.config(command=self.Sales_List.yview)
        self.Sales_List.pack(fill=BOTH, expand=True)
        self.Sales_List.bind("<ButtonRelease-1>", self.get_data)

        # ✅ Bill Display (Center)
        bill_Frame = Frame(content_frame, bd=3, relief=RIDGE)
        bill_Frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

        lbl_title2 = Label(bill_Frame, text="Customer Bill Area", font=("goudy old style", 18), bg="orange")
        lbl_title2.pack(side=TOP, fill=X)

        scrolly2 = Scrollbar(bill_Frame, orient=VERTICAL)

        # ✅ Make Bill Text Fit Perfectly
        self.bill_area = Text(
            bill_Frame, 
            bg="lightyellow",
            font=("Courier", 12),  # Fixed-width font for proper alignment
            wrap="word",  # Prevents words from breaking in half
            padx=5,  # Adds padding for better visibility
            yscrollcommand=scrolly2.set
        )

        self.bill_area.pack(fill=BOTH, expand=True, padx=5, pady=5)
        scrolly2.pack(side=RIGHT, fill=Y)
        scrolly2.config(command=self.bill_area.yview)

        # ✅ Image (Right Side)
        image_frame = Frame(content_frame, bg="white", bd=2, relief=RIDGE)
        image_frame.grid(row=0, column=2, padx=10, pady=5, sticky="ns")

        self.bill_photo = Image.open(cat2)
        self.bill_photo = self.bill_photo.resize((400, 300))
        self.bill_photo = ImageTk.PhotoImage(self.bill_photo)

        lbl_image = Label(image_frame, image=self.bill_photo, bd=2, relief=RIDGE)
        lbl_image.pack(fill=BOTH, expand=True)

        # ✅ Grid Configuration for Responsiveness
        content_frame.grid_columnconfigure(1, weight=1)  # Bill Display should expand
        content_frame.grid_columnconfigure(2, weight=1)  # Image should expand
        content_frame.grid_rowconfigure(0, weight=1)

        self.show()

    # --------------------------------------------------
    def show(self):
        """Displays available bills in the listbox."""
        self.blll_list.clear()
        self.Sales_List.delete(0, END)

        try:
            for i in os.listdir(BILL_DIR):
                if i.endswith('.txt'):
                    self.Sales_List.insert(END, i)
                    self.blll_list.append(i.split('.')[0])
        except Exception as e:
            messagebox.showerror("Error", f"Error loading bills: {str(e)}", parent=self)

    def get_data(self, ev):
        """Displays the content of a selected bill."""
        try:
            index_ = self.Sales_List.curselection()
            if not index_:
                return

            file_name = self.Sales_List.get(index_)
            file_path = os.path.join(BILL_DIR, file_name)

            self.bill_area.delete('1.0', END)

            with open(file_path, 'r') as fp:
                self.bill_area.insert(END, fp.read())

        except Exception as e:
            messagebox.showerror("Error", f"Error opening bill: {str(e)}", parent=self)

    def search(self):
        """Searches for a specific invoice and displays its content."""
        invoice_no = self.var_invoice.get().strip()

        if not invoice_no:
            messagebox.showerror("Error", "Invoice No. should be required", parent=self)
            return

        file_name = f"{invoice_no}.txt"
        file_path = os.path.join(BILL_DIR, file_name)

        if os.path.exists(file_path):
            self.bill_area.delete('1.0', END)
            with open(file_path, 'r') as fp:
                self.bill_area.insert(END, fp.read())
        else:
            messagebox.showerror("Error", "Invalid Invoice No.", parent=self)

    def clear(self):
        """Clears the bill area and refreshes the bill list."""
        self.show()
        self.bill_area.delete('1.0', END)
