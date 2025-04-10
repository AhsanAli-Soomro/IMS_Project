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
class employeeClass(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg="white")
        self.pack(fill=BOTH, expand=True)

        # ------------ All Variables --------------
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()
        self.var_emp_id = StringVar()
        self.var_gender = StringVar()
        self.var_contact = StringVar()
        self.var_name = StringVar()
        self.var_dob = StringVar()
        self.var_doj = StringVar()
        self.var_email = StringVar()
        self.var_pass = StringVar()
        self.var_utype = StringVar()
        self.var_salary = StringVar()

        # ------------ Title Label --------------
        Label(self, text="Employee Management", font=("Arial", 20, "bold"), 
            bg="#0f4d7d", fg="white", padx=20, pady=10).pack(fill=X, anchor=CENTER)

        # ---------- Form Frame -------------
        form_frame = Frame(self, bg="white", bd=2, relief=RIDGE)
        form_frame.place(relx=0.05, rely=0.10, relwidth=0.9, relheight=0.40)  # ✅ Centered form

        # ---------- Labels & Input Fields (No Changes) ----------
        labels = ["Emp ID", "Name", "Email", "Address", "Gender", "D.O.B.", "Password", 
                "Salary", "Contact", "D.O.J.", "User Type"]

        input_vars = [self.var_emp_id, self.var_name, self.var_email, None, self.var_gender, 
                    self.var_dob, self.var_pass, self.var_salary, self.var_contact, 
                    self.var_doj, self.var_utype]

        for i in range(4):  # ✅ Creating 4 rows
            for j in range(3):  # ✅ 3 columns per row
                index = i * 3 + j
                if index >= len(labels):  # ✅ Prevent Index Error
                    break
                
                Label(form_frame, text=labels[index], font=("goudy old style", 15), bg="white").grid(row=i, column=j*2, padx=10, pady=10, sticky=W)

                if labels[index] == "User Type":
                    cmb_utype = ttk.Combobox(form_frame, textvariable=self.var_utype, values=("Admin", "Employee"),
                                            state='readonly', justify=CENTER, font=("goudy old style", 15))
                    cmb_utype.grid(row=i, column=j*2 + 1, padx=10, pady=10, sticky=W)
                    cmb_utype.current(0)
                elif labels[index] == "Gender":
                    cmb_gender = ttk.Combobox(form_frame, textvariable=self.var_gender, values=("Select", "Male", "Female", "Other"),
                                            state='readonly', justify=CENTER, font=("goudy old style", 15))
                    cmb_gender.grid(row=i, column=j*2 + 1, padx=10, pady=10, sticky=W)
                    cmb_gender.current(0)
                elif labels[index] == "Address":
                    self.txt_address = Text(form_frame, font=("goudy old style", 15), bg="lightyellow", height=3, width=30)
                    self.txt_address.grid(row=i, column=j*2 + 1, padx=10, pady=10, sticky=W)
                else:
                    Entry(form_frame, textvariable=input_vars[index], font=("goudy old style", 15), bg="lightyellow").grid(row=i, column=j*2 + 1, padx=10, pady=10, sticky=W)

        # ---------- Buttons (Using Label Instead of Button) ----------
        btn_frame = Frame(self, bg="white")
        btn_frame.place(relx=0.30, rely=0.55, relwidth=0.4, height=50)

        buttons = [
            ("Save", self.add, "#2196f3"),
            ("Update", self.update, "#4caf50"),
            ("Delete", self.delete, "#f44336"),
            ("Clear", self.clear, "#607d8b"),
        ]

        for i, (text, cmd, color) in enumerate(buttons):
            btn = Label(btn_frame, text=text, cursor="hand2",
                        font=("goudy old style", 15, "bold"), bg=color, fg="white",
                        relief=RAISED, padx=10, pady=5)

            # ✅ Add Click Event
            btn.bind("<Button-1>", lambda e, func=cmd: func())  # Call respective function

            # ✅ Add Hover Effect
            btn.bind("<Enter>", lambda e, b=btn, c=color: b.config(bg=self.darken_color(c)))  # Darker hover effect
            btn.bind("<Leave>", lambda e, b=btn, c=color: b.config(bg=c))  # Restore original color

            btn.grid(row=0, column=i, padx=10, pady=10)


        # ------------ Employee Table -------------
        self.create_table()

    def create_table(self):
        """Create the Employee Table (Responsive)"""
        emp_frame = Frame(self, bd=3, relief=RIDGE)
        emp_frame.place(relx=0, rely=0.65, relwidth=1, relheight=0.35)

        scrolly = Scrollbar(emp_frame, orient=VERTICAL)
        scrollx = Scrollbar(emp_frame, orient=HORIZONTAL)

        self.EmployeeTable = ttk.Treeview(emp_frame, columns=(
            "eid", "name", "email", "gender", "contact", "dob", "doj",
            "pass", "utype", "address", "salary"),
            yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.EmployeeTable.xview)
        scrolly.config(command=self.EmployeeTable.yview)

        for col in self.EmployeeTable["columns"]:
            self.EmployeeTable.heading(col, text=col.upper())
            self.EmployeeTable.column(col, width=100)

        self.EmployeeTable["show"] = "headings"
        self.EmployeeTable.pack(fill=BOTH, expand=True)
        self.EmployeeTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()



#-----------------------------------------------------------------------------------------------------
    def add(self):
        con = sqlite3.connect(resource_path("ims.db"))
        cur=con.cursor()
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error","Employee ID must be required",parent=self)
            else:
                cur.execute("Select * from employee where eid=?",(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This Employee ID is already assigned",parent=self)
                else:
                    cur.execute("insert into employee(eid,name,email,gender,contact,dob,doj,pass,utype,address,salary) values(?,?,?,?,?,?,?,?,?,?,?)",(
                        self.var_emp_id.get(),
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_gender.get(),
                        self.var_contact.get(),
                        self.var_dob.get(),
                        self.var_doj.get(),
                        self.var_pass.get(),
                        self.var_utype.get(),
                        self.txt_address.get('1.0',END),
                        self.var_salary.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Employee Added Successfully",parent=self)
                    self.clear()
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def show(self):
        con = sqlite3.connect(resource_path("ims.db"))
        cur=con.cursor()
        try:
            cur.execute("select * from employee")
            rows=cur.fetchall()
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in rows:
                self.EmployeeTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def get_data(self,ev):
        f=self.EmployeeTable.focus()
        content=(self.EmployeeTable.item(f))
        row=content['values']
        self.var_emp_id.set(row[0])
        self.var_name.set(row[1])
        self.var_email.set(row[2])
        self.var_gender.set(row[3])
        self.var_contact.set(row[4])
        self.var_dob.set(row[5])
        self.var_doj.set(row[6])
        self.var_pass.set(row[7])
        self.var_utype.set(row[8])
        self.txt_address.delete('1.0',END)
        self.txt_address.insert(END,row[9])
        self.var_salary.set(row[10])


    def darken_color(self, hex_color, factor=0.85):
        """Darkens a hex color by multiplying its RGB values."""
        hex_color = hex_color.lstrip("#")
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        darkened_rgb = tuple(int(c * factor) for c in rgb)
        return f"#{darkened_rgb[0]:02x}{darkened_rgb[1]:02x}{darkened_rgb[2]:02x}"


    def update(self):
        con = sqlite3.connect(resource_path("ims.db"))
        cur=con.cursor()
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error","Employee ID must be required",parent=self)
            else:
                cur.execute("Select * from employee where eid=?",(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Employee ID",parent=self)
                else:
                    cur.execute("update employee set name=?,email=?,gender=?,contact=?,dob=?,doj=?,pass=?,utype=?,address=?,salary=? where eid=?",(
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_gender.get(),
                        self.var_contact.get(),
                        self.var_dob.get(),
                        self.var_doj.get(),
                        self.var_pass.get(),
                        self.var_utype.get(),
                        self.txt_address.get('1.0',END),
                        self.var_salary.get(),
                        self.var_emp_id.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Employee Updated Successfully",parent=self)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def delete(self):
        con = sqlite3.connect(resource_path("ims.db"))
        cur=con.cursor()
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error","Employee ID must be required",parent=self)
            else:
                cur.execute("Select * from employee where eid=?",(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Employee ID",parent=self)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self)
                    if op==True:
                        cur.execute("delete from employee where eid=?",(self.var_emp_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Employee Deleted Successfully",parent=self)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def clear(self):
        self.var_emp_id.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_contact.set("")
        self.var_dob.set("")
        self.var_doj.set("")
        self.var_pass.set("")
        self.var_utype.set("Admin")
        self.txt_address.delete('1.0',END)
        self.var_salary.set("")
        self.var_searchby.set("Select")
        self.var_searchtxt.set("")
        self.show()

    def search(self):
        con = sqlite3.connect(resource_path("ims.db"))
        cur=con.cursor()
        try:
            if self.var_searchby.get()=="Select":
                messagebox.showerror("Error","Select Search By option",parent=self)
            elif self.var_searchtxt.get()=="":
                messagebox.showerror("Error","Search input should be required",parent=self)
            else:
                cur.execute("select * from employee where "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                    for row in rows:
                        self.EmployeeTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found!!!",parent=self)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")