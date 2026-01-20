import tkinter as tk
from tkinter import ttk
from gui.baseWindow import BaseWindow
from bff.enums import PlayerRole, BattingStyle, BowlingStyle


class PlayerManagementWindow(BaseWindow):
    def __init__(self, window, parent):
        super().__init__(window)
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
                  ).pack(pady=20)
        tk.Button(main_frame,
                  text="DELETE PLAYER",
                  width=15,
                  height=3,
                  ).pack(pady=30)

    def open_create_player_page(self):
        self.window.withdraw()
        CreatePlayerWindow(tk.Toplevel(self.window), self.window)




    def go_back(self):
        self.window.destroy()
        self.parent.deiconify()


class CreatePlayerWindow(BaseWindow):
    def __init__(self, window, parent):
        super().__init__(window)
        self.window = window
        self.parent = parent
        self.window.title("SS - CREATE PLAYER")
        self.center_window(800, 600)
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

        save_btn = tk.Button(footer, text="SAVE", command="",width=15 )
        save_btn.pack(side=tk.RIGHT, padx=20, pady=20)

    #def save_player(self):
     #   first_name = self.first_name_input.get().strip()
      #  last_name = self.last_name_input.get().strip()




    def go_back(self):
        self.window.destroy()
        self.parent.deiconify()






