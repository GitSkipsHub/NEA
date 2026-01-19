import tkinter as tk
from tkinter import messagebox
from gui.baseWindow import BaseWindow
from bff.models import Account
from bff.database import AccountDB


class RegistrationWindow(BaseWindow):
    def __init__(self, window, parent):
        #Inherits BaseWindow
        super().__init__(window)
        self.window = window #Current GUI Window
        self.parent = parent #Previous 'Parent' Window
        self.window.title("SS - REGISTRATION")
        self.center_window(800, 500)
        #Creates Instance of AccountDB class
        self.account_db = AccountDB()
        self.create_widgets()

    def create_widgets(self):
        main_frame = self.create_main_frame()
        self.create_header(main_frame, "REGISTRATION")

        form = tk.Frame(main_frame)
        form.pack(pady=80)

        #USERNAME INPUT
        tk.Label(form, text="USERNAME : ", ).grid(column=0, row=0, pady=10, sticky="e")
        self.username_input = tk.Entry(form)
        self.username_input.grid(column=1, row=0, pady=10)

        #PASSWORD INPUT
        tk.Label(form, text="PASSWORD : ", ).grid(column=0, row=1, pady=10, sticky="e")
        self.password_input = tk.Entry(form, show="*")
        self.password_input.grid(column=1, row=1, pady=10)

        #CONFIRM PASSWORD INPUT
        tk.Label(form, text="CONFIRM PASSWORD : ", ).grid(column=0, row=2, pady=10, sticky="e")
        self.confirm_password_input = tk.Entry(form, show="*")
        self.confirm_password_input.grid(column=1, row=2, pady=10)

        #Footer Created to Position Back Button at Bottom of Screen
        footer = tk.Frame(main_frame)
        footer.pack(fill=tk.X, side=tk.BOTTOM)

        #Calls create_back_btn function from BaseWindow
        back_btn = self.create_back_btn(footer, self.go_back) #Takes footer as parent to show where to position Back Btn
        back_btn.pack(side=tk.LEFT, padx=20, pady=20, )

        tk.Button(footer, text="REGISTER", width=15, command=self.register, ).pack(side=tk.RIGHT, padx=20, pady=20)

    def register(self):
        username = self.username_input.get().strip() #Removes white spaces in username
        #No Need for Strip for Password as Spaces don't Count
        password = self.password_input.get()
        confirm_password = self.confirm_password_input.get()

        if not username or not password:
            messagebox.showerror("ERROR", "ENTER VALID CREDENTIALS")
            return

        if len(username) < 2:
            messagebox.showerror("ERROR", "USERNAME MUST BE AT LEAST 2 CHARACTERS LONG")
            return

        if len(password) < 8:
            messagebox.showerror("ERROR", "PASSWORD MUST BE AT LEAST 8 CHARACTERS LONG")
            return

        if not confirm_password:
            messagebox.showerror("ERROR", "CONFIRM PASSWORD")
            return

        if password != confirm_password:
            messagebox.showerror("ERROR", "PASSWORDS DO NOT MATCH")
            return

        if self.account_db.username_exists(username):
            messagebox.showerror("ERROR", "USERNAME ALREADY EXISTS")
            return

        hashed_password = Account.hash_password(password)

        if self.account_db.create_account(username, hashed_password):
            messagebox.showinfo("SUCCESS", "ACCOUNT CREATED")
            self.go_back()
            return

        else:
            messagebox.showerror("ERROR", "COULDN'T CREATE ACCOUNT")
            return

    #back_command Function
    def go_back(self):
        self.window.destroy()
        self.parent.deiconify() #Make previous window visible again


class LoginWindow(BaseWindow):
    def __init__(self, window, parent):
        super().__init__(window)
        self.window = window
        self.parent = parent
        self.window.title("SS - LOGIN")
        self.center_window(800, 500)
        self.account_db = AccountDB()
        self.create_widgets()

    def create_widgets(self):
        main_frame = self.create_main_frame()
        self.create_header(main_frame, "LOGIN")

        form = tk.Frame(main_frame)
        form.pack(pady=100)

        tk.Label(form, text="USERNAME : ").grid(column=0, row=0, pady=10, sticky="e")
        self.username_input = tk.Entry(form)
        self.username_input.grid(column=1, row=0, pady=10)

        tk.Label(form, text="PASSWORD : ").grid(column=0, row=1, pady=10, sticky="e")
        self.password_input = tk.Entry(form, show="*")
        self.password_input.grid(column=1, row=1, pady=10, )

        footer = tk.Frame(main_frame)
        footer.pack(fill=tk.X, side=tk.BOTTOM)

        back_btn = self.create_back_btn(footer, self.go_back)
        back_btn.pack(side=tk.LEFT, padx=20, pady=20)

        tk.Button(footer, text="LOGIN", width=15, command=self.login, ).pack(side=tk.RIGHT, padx=20, pady=20)

    #LOGIN FUNCTION VALIDATION CHECKS
    def login(self):
        username = self.username_input.get().strip()
        password = self.password_input.get()
        if not username or not password:
            messagebox.showerror("ERROR", "ENTER VALID CREDENTIALS")
            return

        #Finds existing usernames in the database
        account = self.account_db.find_account(username)

        if not account:
            messagebox.showerror("ERROR", "USERNAME NOT FOUND")
            return

        #Account from models class and checks if passwords match
        if not Account.verify_password(password, account["hashed_password"]):
            messagebox.showerror("ERROR", "INCORRECT PASSWORD")
            return

        else:
            messagebox.showerror("SUCCESS", "ACCESS GRANTED")
            self.open_home_page()
            return

    def open_home_page(self):
        from gui.home import HomePage
        username = self.username_input.get().strip() #Need username for HomePage Welcome
        self.window.destroy()
        new = tk.Toplevel(self.parent) #Creates new TopLevel Window from previous page
        HomePage(new, None, username) #

    def go_back(self):
        self.window.destroy()
        self.parent.deiconify()

