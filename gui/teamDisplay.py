import tkinter as tk
from tkinter import ttk, messagebox

from gui.baseWindow import BaseWindow

class TeamDisplay(BaseWindow):
    def __init__(self, window, parent, username, generated_team):
        super().__init__(window)
        self.window = window
        self.parent = parent
        self.current_user = username
        self.generated_team = generated_team
        self.window.title("SS - TEAM GENERATION")
        self.center_window(1000, 600)

        self.create_widgets()


    def create_widgets(self):
        main_frame = self.create_main_frame()
        self.create_header(main_frame, "GENERATED TEAM")

        team_frame = tk.Frame(main_frame)
        team_frame.pack(padx=30, pady=30)
        team_frame.configure(highlightcolor="dodger blue", highlightthickness=3)

        team_columns = ["player_name", "player_role", "total_runs", "total_wickets", "total_dismissals"]

        x_scrollbar = ttk.Scrollbar(team_frame, orient="horizontal")
        x_scrollbar.pack(side="bottom", fill="x")

        self.team_tree = ttk.Treeview(team_frame, columns=team_columns, show="headings",height=12,  xscrollcommand=x_scrollbar.set)
        self.team_tree.pack(side="right", fill="both", expand=True)

        x_scrollbar.config(command=self.team_tree.xview)


        self.team_tree.heading("player_name", text="Player Name")
        self.team_tree.heading("player_role", text="Player Role")
        self.team_tree.heading("total_runs", text="Total Runs")
        self.team_tree.heading("total_wickets", text="Total Wickets")
        self.team_tree.heading("total_dismissals", text="Total Dismissals")

        self.team_tree.column("player_name", width=200, anchor="center")
        self.team_tree.column("player_role", width=200, anchor="center")
        self.team_tree.column("total_runs", width=200, anchor="center")
        self.team_tree.column("total_wickets", width=200, anchor="center")
        self.team_tree.column("total_dismissals", width=200, anchor="center")

        self.add_player_to_team()


    def add_player_to_team(self):
        for player in self.generated_team:
            self.team_tree.insert(
                "",
                "end",
                values=(
                    player.get("player_name", ""),
                    player.get("player_role", ""),
                    player.get("total_runs", ""),
                    player.get("total_wickets", ""),
                    player.get("total_dismissals", ""),
                ))








