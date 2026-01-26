import tkinter as tk
from tkinter import ttk, messagebox
from gui.baseWindow import BaseWindow
from bff.database import PlayerDB
from bff.enums import PlayerRole, BattingStyle, BowlingStyle


class PlayerManagementWindow(BaseWindow):
    def __init__(self, window, parent, username):
        super().__init__(window)
        self.current_user = username
        self.window = window
        self.parent = parent

        self.window.title("SS - PLAYER MANAGEMENT")
        self.center_window(800, 600)
        self.create_widgets()

    def create_widgets(self):
        main_frame = self.create_main_frame()
        self.create_header(main_frame, "PLAYER MANAGEMENT")

        footer = tk.Frame(main_frame)
        footer.pack(fill=tk.X, side=tk.BOTTOM)

        back_btn = self.create_back_btn(footer, self.go_back)
        back_btn.pack(side=tk.LEFT, padx=20, pady=20)

        tk.Button(main_frame,
                  text="CREATE PLAYER",
                  width=15,
                  height=3,
                  command=self.open_create_player_page,
                  ).pack(pady=30)

        tk.Button(main_frame,
                  text="UPDATE PLAYER",
                  width=15,
                  height=3,
                  command=self.open_update_player_window
                  ).pack(pady=20)
        tk.Button(main_frame,
                  text="DELETE PLAYER",
                  width=15,
                  height=3,
                  ).pack(pady=30)

    def open_create_player_page(self):
        self.window.withdraw()
        CreatePlayerWindow(tk.Toplevel(self.window), self.window, self.current_user)

    def open_update_player_window(self):
        self.window.withdraw()
        UpdatePlayerWindow(tk.Toplevel(self.window), self.window, self.current_user)

    def go_back(self):
        self.window.destroy()
        self.parent.deiconify()


class CreatePlayerWindow(BaseWindow):
    def __init__(self, window, parent, username):
        super().__init__(window)
        self.window = window
        self.parent = parent
        self.window.title("SS - CREATE PLAYER")
        self.center_window(800, 600)
        self.current_user = username
        self.player_db = PlayerDB()
        self.create_widgets()

    def create_widgets(self):

        main_frame = self.create_main_frame()
        self.create_header(main_frame, "PLAYER CREATION")

        form = tk.Frame(main_frame)
        form.pack(pady=50)

        footer = tk.Frame(main_frame)
        footer.pack(fill=tk.X, side=tk.BOTTOM)

        tk.Label(form, text="FIRST NAME : ").grid(column=0, row=0, pady=10, sticky="e")
        self.first_name_input = tk.Entry(form)
        self.first_name_input.configure(highlightthickness=3, highlightbackground="dodger blue")
        self.first_name_input.grid(column=1, row=0, pady=10)

        tk.Label(form, text="LAST NAME : ").grid(column=0, row=1, pady=10, sticky="e")
        self.last_name_input = tk.Entry(form)
        self.last_name_input.configure(highlightthickness=3, highlightbackground="dodger blue")
        self.last_name_input.grid(column=1, row=1, pady=10)

        tk.Label(form, text="DATE OF BIRTH (YYYY-MM-DD): ").grid(column=0, row=2, pady=10, sticky="e")
        self.dob_input = tk.Entry(form)
        self.dob_input.configure(highlightthickness=3, highlightbackground="dodger blue")
        self.dob_input.grid(column=1, row=2, pady=10)

        # tk.Label(form, text="PLAYER ROLE: ").grid(column=0, row=3, pady=10, sticky="e")
        # self.player_role_var = tk.StringVar()
        # player_role_values = PlayerRole.list_values()
        # ttk.Combobox(form,
        #              textvariable=self.player_role_var,
        #              values=player_role_values,
        #              state="readonly",
        #              width=20,
        #              ).grid(column=1, row=3, pady=10)
        #
        # tk.Label(form, text="BATTING STYLE: ").grid(column=0, row=4, pady=10, sticky="e")
        # self.batting_style_var = tk.StringVar()
        # batting_style_values = BattingStyle.list_values()
        # ttk.Combobox(form,
        #              textvariable=self.batting_style_var,
        #              values=batting_style_values,
        #              state="readonly",
        #              width=20,
        #              ).grid(column=1, row=4, pady=10)
        #
        # tk.Label(form, text="BOWLING STYLE: ").grid(column=0, row=5, pady=10, sticky="e")
        # self.bowling_style_var = tk.StringVar()
        # bowling_style_values = BowlingStyle.list_values()
        # ttk.Combobox(form,
        #              textvariable=self.bowling_style_var,
        #              values=bowling_style_values,
        #              state="readonly",
        #              width=20,
        #              ).grid(column=1, row=5, pady=10)


        self.player_role_var = tk.StringVar()
        self.create_dropdown(
            parent=form,
            text="PLAYER ROLE: ",
            variable=self.player_role_var,
            values=PlayerRole.list_values(),
            row=3,
        )

        self.batting_style_var = tk.StringVar()
        self.create_dropdown(
            parent=form,
            text="BATTING STYLE: ",
            variable=self.batting_style_var,
            values=BattingStyle.list_values(),
            row=4,
        )

        self.bowling_style_var = tk.StringVar()
        self.create_dropdown(
            parent=form,
            text="BOWLING STYLE: ",
            variable=self.bowling_style_var,
            values=BowlingStyle.list_values(),
            row=5,
        )


        back_btn = self.create_back_btn(footer, self.go_back)
        back_btn.pack(side=tk.LEFT, padx=20, pady=20)

        #tk.Button(footer, text="SAVE", width=15,).pack(side=tk.RIGHT, padx=20, pady=20)

        save_btn = tk.Button(footer, text="SAVE", command= self.save_player, width=15 )
        save_btn.pack(side=tk.RIGHT, padx=20, pady=20)

    def save_player(self):
        first_name = self.first_name_input.get().strip()
        last_name = self.last_name_input.get().strip()
        dob = self.dob_input.get().strip()
        player_role = self.player_role_var.get().strip()
        batting_style = self.batting_style_var.get().strip()
        bowling_style = self.bowling_style_var.get().strip()

        if not first_name or not last_name or not dob or not player_role or not bowling_style or not batting_style:
            messagebox.showerror("Error", "Please fill in all required fields")
            return

        player_data = {
            "first_name": first_name,
            "last_name": last_name,
            "date_of_birth": dob,
            "player_role": player_role,
            "batting_style": batting_style,
            "bowling_style": bowling_style,
        }

        if self.player_db.create_player(self.current_user, player_data):
            messagebox.showinfo("SUCCESS", "Player Created")
            self.go_back()
            return
        else:
            messagebox.showerror("ERROR", "Failed to Create Player")
            return


    def go_back(self):
        self.window.destroy()
        self.parent.deiconify()


class UpdatePlayerWindow(BaseWindow):
    def __init__(self, window, parent, username):
        super().__init__(window)
        self.window = window
        self.parent = parent
        self.current_user = username
        self.player_db = PlayerDB
        self.window.title("SS - PLAYER MANAGEMENT")
        self.center_window(900, 700)
        self.create_widgets()


    def create_widgets(self):

        main_frame = self.create_main_frame()
        self.create_header(main_frame, "UPDATE PLAYER")
        self.create_sub_header(main_frame, "SEARCH PLAYER")

        footer = tk.Frame(main_frame)
        footer.pack(fill=tk.X, side=tk.BOTTOM)

        back_btn = self.create_back_btn(footer, self.go_back)
        back_btn.pack(side=tk.LEFT, padx=20, pady=20)

        update_button = tk.Button(footer, text="UPDATE PLAYER", command=self.update_player, width=15)
        update_button.pack(side=tk.RIGHT, pady=10, padx=10)

        search_button = tk.Button(footer, text="SEARCH", command=self.search_player, width=15)
        search_button.pack(side=tk.BOTTOM, padx=10, pady=10)

        search_frame = tk.Frame(main_frame)
        search_frame.pack(pady=40)

        buttons_frame = tk.Frame(search_frame)
        buttons_frame.grid(row=1, column=3, padx=100, pady=20, sticky=tk.E)

        tk.Label(search_frame, text="FIRST NAME: ").grid(row=0, column=0)
        self.search__fname_var = tk.StringVar()
        self.first_name_input = tk.Entry(search_frame, textvariable=self.search__fname_var)
        self.first_name_input.configure(highlightthickness=3, highlightbackground="dodger blue")
        self.first_name_input.grid(row=0, column=1, pady=10)

        tk.Label(search_frame, text="LAST NAME: ").grid(row=1, column=0)
        self.search_lname_var = tk.StringVar()
        self.last_name_input = tk.Entry(search_frame, textvariable=self.search_lname_var)
        self.last_name_input.configure(highlightthickness=3, highlightbackground="dodger blue")
        self.last_name_input.grid(row=1, column=1, pady=10)

        self.tree = ttk.Treeview(main_frame, columns=("Created Date", "First Name", "Last Name", "Player Role"))
        self.tree.grid(row=2, column=0, columnspan=3, pady=10, padx=10)

        self.tree.heading("create_date", text="Created Date")
        self.tree.heading("first_name", text="First Name")
        self.tree.heading("last_name", text="Last Name")
        self.tree.heading("player_role", text="Player Role")

        self.tree.column("created_date", width=90)
        self.tree.column("first_name", width=120)
        self.tree.column("last_name", width=150)
        self.tree.column("player_role", width=100)




    def search_player(self):
        self.tree.delete(*self.tree.get_children())
        fname_query = {"first_name": {"$regex": self.search__fname_var.get(), "$options": "i"}}
        lname_query = {"last_name": {"$regex": self.search_lname_var.get(), "$options": "i"}}

        query = {}
        if self.search__fname_var.get():
            query.update(fname_query)
        if self.search_lname_var.get():
            query.update(lname_query)

        if query:
            sort_criteria = [("first_name", 1)]

        projection = {"id": 1, "first_name": 1, "last_name": 1 }





    def update_player(self):
        pass









    def go_back(self):
        self.window.destroy()
        self.parent.deiconify()













