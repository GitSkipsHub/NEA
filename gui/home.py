import tkinter as tk
from gui.baseWindow import BaseWindow

class HomePage(BaseWindow):
    def __init__(self, window, parent, username):
        super().__init__(window)
        self.current_user = username
        self.window = window
        self.parent = parent
        self.window.title("SS - HOME PAGE")
        self.center_window(800, 550)

        self.create_widgets()

    def create_widgets(self):
        main_frame = self.create_main_frame()

        tk.Label(main_frame,
                 text=f"WELCOME BACK {self.current_user} !",
                 underline=0,
                 font=("Arial", 20  , "bold"),
                 fg="dodger Blue",
                 borderwidth=5,
                 ).pack(fill=tk.BOTH, expand= True, pady=5, padx=10)


        content_frame = tk.Frame(main_frame, borderwidth=1, relief="solid")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=12)

        self.create_header(content_frame, text="HOME PAGE")

        tk.Button(content_frame,
                  text="PLAYER MANAGEMENT",
                  width=15,
                  height=3,
                  command=self.open_player_management_page,
                  ).pack(pady=12)

        tk.Button(content_frame,
                  text="TEAM GENERATION",
                  width=15,
                  height=3,
                  command=self.open_team_generation_page,
                  ).pack(pady=12)

        tk.Button(content_frame,
                  text="MATCH MANAGEMENT",
                  width=15,
                  height=3,
                  command=self.open_match_management_page,
                  ).pack(pady=19)

        tk.Button(content_frame,
                  text="LOGOUT",
                  width=15,
                  height=3,
                  command=self.log_out,
                  ).pack(pady=12)



    def open_player_management_page(self):
        from gui.player import PlayerManagementWindow
        self.window.withdraw()
        PlayerManagementWindow(tk.Toplevel(self.window), self.window, self.current_user)

    def open_team_generation_page(self):
        from gui.teamGen import FixtureDetailsPage
        self.window.withdraw()
        FixtureDetailsPage(tk.Toplevel(self.window), self.window, self.current_user)

    def open_match_management_page(self):
        from gui.match import MatchManagementPage
        self.window.withdraw()
        MatchManagementPage(tk.Toplevel(self.window), self.window)

    def log_out(self):
        pass





    #     footer = tk.Frame(main_frame)
    #     footer.pack(fill=tk.X, side=tk.BOTTOM)
    #
    #     back_btn = self.create_back_btn(footer, self.go_back)
    #     back_btn.pack(side=tk.LEFT, padx=20, pady=20)
    #
    # def go_back(self):
    #     self.window.destroy()
    #     self.parent.deiconify()



