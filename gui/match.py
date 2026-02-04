import tkinter as tk
from tkinter import ttk, messagebox, Canvas
from datetime import datetime
from gui.baseWindow import BaseWindow
from bff.database import MatchDB, PlayerDB
from bff.enums import PlayerRole, BowlingStyle, BattingStyle, MatchFormat, Venue, Result, MatchType
from bff.models import Batting, Bowling, Fielding


class MatchManagementPage(BaseWindow):
    def __init__(self, window, parent, username):
        super().__init__(window)
        self.window = window
        self.parent = parent
        self.current_user = username

        self.window.title("SS - MATCH MANAGEMENT")
        self.center_window(800, 600)

        self.create_widgets()

    def create_widgets(self):
        main_frame = self.create_main_frame()
        self.create_header(main_frame, "MATCH MANAGEMENT")

        footer = tk.Frame(main_frame)
        footer.pack(fill="x", side="bottom")

        back_btn = self.create_back_btn(footer, self.go_back)
        back_btn.pack(side=tk.LEFT, padx=20, pady=20)

        #Navigation Buttons
        tk.Button(main_frame,
                  text="CREATE MATCH",
                  width=15,
                  height=3,
                  command=self.open_create_match_details_page,
                  ).pack(pady=40)

        tk.Button(main_frame,
                  text="UPDATE MATCH",
                  width=15,
                  height=3,
                  ).pack(pady=30)

        tk.Button(main_frame,
                  text="DELETE MATCH",
                  width=15,
                  height=3,
                  ).pack(pady=40)

    def open_create_match_details_page(self):
        self.window.withdraw()
        CreateMatchDetailsPage(tk.Toplevel(self.window), self.window, self.current_user)


    def go_back(self):
        self.window.destroy()
        self.parent.deiconify()


class CreateMatchDetailsPage(BaseWindow):
    def __init__(self, window, parent, username):
        super().__init__(window)
        self.window = window
        self.parent = parent
        self.current_user = username

        self.window.title("SS - MATCH CREATION")
        self.center_window(850,650)

        self.match_db = MatchDB()
        self.created_match_id = None

        self.create_widgets()

    def create_widgets(self):
        main_frame = self.create_main_frame()
        self.create_header(main_frame, "CREATE MATCH")
        self.create_sub_header(main_frame, "MATCH DETAILS")

        form = tk.Frame(main_frame)
        form.pack(pady=10)

        self.match_type_var = tk.StringVar()
        self.create_dropdown(
            parent=form,
            text="MATCH TYPE: ",
            variable=self.match_type_var,
            values=MatchType.list_values(),
            row=0
        )

        self.match_format_var = tk.StringVar()
        self.create_dropdown(
            parent=form,
            text="MATCH FORMAT: ",
            variable=self.match_format_var,
            values=MatchFormat.list_values(),
            row=1
        )

        self.venue_var = tk.StringVar()
        self.create_dropdown(
            parent=form,
            text="VENUE: ",
            variable=self.venue_var,
            values=Venue.list_values(),
            row=2
        )

        self.result_var = tk.StringVar()
        self.create_dropdown(
            parent=form,
            text="RESULT: ",
            variable=self.result_var,
            values=Result.list_values(),
            row=3
        )

        tk.Label(form, text="GROUND NAME: ").grid(column=0, row=4, pady=10, sticky="e")
        self.ground_name_input = tk.Entry(form)
        self.ground_name_input.configure(highlightthickness=3, highlightbackground="dodger blue")
        self.ground_name_input.grid(column=1, row=4, pady=10)

        tk.Label(form, text="OPPOSITION: ").grid(column=0, row=5, pady=10, sticky="e")
        self.opposition_input = tk.Entry(form)
        self.opposition_input.configure(highlightthickness=3, highlightbackground="dodger blue")
        self.opposition_input.grid(column=1, row=5, pady=10)

        tk.Label(form, text="DATE (YYYY-MM-DD): ").grid(column=0, row=6, pady=10, sticky="e")
        self.date_input = tk.Entry(form)
        self.date_input.configure(highlightthickness=3, highlightbackground="dodger blue")
        self.date_input.grid(column=1, row=6, pady=10)


        footer = tk.Frame(main_frame)
        footer.pack(fill="x", side="bottom")

        save_btn = tk.Button(footer, text="SAVE", command=self.save_match_details_and_continue, width=15)
        save_btn.pack(side="right", padx=20, pady=20)

        back_btn = self.create_back_btn(footer, self.go_back)
        back_btn.pack(side=tk.LEFT, padx=20, pady=20)


    def save_match_details_and_continue(self):

        #Strips all inputs
        match_type_value = self.match_type_var.get().strip()
        match_format_value = self.match_format_var.get().strip()
        venue_value = self.venue_var.get().strip()
        result = self.result_var.get().strip()
        ground_name = self.ground_name_input.get().strip()
        opposition = self.opposition_input.get().strip()
        date = self.date_input.get().strip()

        if (not match_type_value or not match_format_value or not venue_value or not result or not ground_name or not
        opposition or not date):
                messagebox.showerror("Error", "Please fill in all required fields")
                return

        #Datetime validation
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("ERROR", "DOB must be in YYYY-MM-DD format (e.g., 2007-04-19)")
            return

        match_data = {
            "match_type": MatchType.get_key(match_type_value), #stores enum key into mongo
            "match_format": MatchFormat.get_key(match_format_value),
            "venue": Venue.get_key(venue_value),
            "result": result,
            "ground_name": ground_name,
            "opposition": opposition,
            "date": date,
        }

        match_id = self.match_db.create_match(self.current_user, match_data)

        if match_id is None:
            messagebox.showerror("ERROR", "FAILED TO CREATE MATCH")

        self.created_match_id = match_id #stores id of match for it to be used later in update or delete functions

        self.window.withdraw()
        SelectTeamPage(tk.Toplevel(self.window), self.window, self.current_user, self.created_match_id)



    def go_back(self):
        self.window.destroy()
        self.parent.deiconify()


class SelectTeamPage(BaseWindow):
    def __init__(self, window, parent, username, created_match_id):
        super().__init__(window)
        self.window = window
        self.parent = parent
        self.current_user = username
        self.match_id = created_match_id
        self.match_db = MatchDB()
        self.player_db = PlayerDB()
        self.all_players = self.player_db.get_all_players(username)
        self.selected_team = [] #list of all selected players (team)
        self.window.title("SS - MATCH MANAGEMENT")
        self.center_window(1500, 900)

        self.create_widgets()

    def create_widgets(self):

        main_frame = self.create_main_frame()
        self.create_header(main_frame, "CREATE MATCH")
        self.create_sub_header(main_frame, "SELECT TEAM")

        footer = tk.Frame(main_frame)
        footer.pack(fill="x", side="bottom")

        back_btn = self.create_back_btn(footer, self.go_back)
        back_btn.pack(side=tk.LEFT, padx=10, pady=10)

        save_team_btn = tk.Button(footer, text="SAVE TEAM", width=15, command=self.save_team_and_continue)
        save_team_btn.pack(side="right", padx=20, pady=20)

        content_frame = tk.Frame(main_frame, highlightbackground="dodger blue", highlightthickness=4)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        left_frame = tk.Frame(content_frame, highlightbackground="white", highlightthickness=2)
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        clear_btn = tk.Button(left_frame, text="CLEAR TEAM", width=15, command=self.clear_team)
        clear_btn.pack(side="bottom", padx=20, pady=20)

        team_frame = tk.Frame(left_frame)
        team_frame.pack(fill="both", expand=True, padx=20, pady=10)

        team_columns = ("position", "player_name")

        self.team_tree = ttk.Treeview(team_frame, columns=team_columns, show="headings", height=12,)
        self.team_tree.pack(fill="both", expand=True)

        self.team_tree.heading("position", text="POS")
        self.team_tree.heading("player_name", text="Player Name")

        self.team_tree.column("position", width=50, anchor="center")
        self.team_tree.column("player_name", width=200, anchor="center")

        self.captain_var = tk.StringVar() #stores what the user selected in the dropdown

        tk.Label(left_frame, text="Captain: ", anchor="e").pack(side="left", padx=10, pady=40)
        self.captain_dropdown = ttk.Combobox(left_frame, textvariable=self.captain_var, width=20, state="readonly")
        self.captain_dropdown.pack(side="left", padx=5, pady=40)

        self.wk_var = tk.StringVar() #stores what the user selected in the dropdown

        tk.Label(left_frame, text="Wicket-Keeper", anchor="e").pack(side="left", padx=10, pady=40)
        self.wk_dropdown = ttk.Combobox(left_frame, textvariable=self.wk_var, width=20, state="readonly")
        self.wk_dropdown.pack(side="left", padx=5, pady=40)

        self.name_to_player_id = {} #dictionary used to translate from dropdown player name to player id

        right_frame = tk.Frame(content_frame, highlightbackground="white", highlightthickness=2)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        tk.Label(right_frame, text="PLAYER SELECTION", font=("Arial", 15, "bold")).pack(padx=25, pady=20, side="top")

        search_frame = tk.Frame(right_frame)
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="SEARCH NAME: ", font=("Arial", 15)).grid(row=1, column=0, padx=10, pady=30, sticky="e")
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.configure(highlightthickness=3, highlightbackground="dodger blue")
        search_entry.grid(row=1, column=1, padx=10, pady=10)

        search_button = tk.Button(search_frame, text="SEARCH", width=15, command=self.search_player)
        search_button.grid(row=1, column=2, padx=30, pady=10)

        table_frame = tk.Frame(right_frame)
        table_frame.pack(fill="both", expand=True, padx=30, pady=5)

        player_columns = ("player_id", "player_name", "player_role", "batting_style", "bowling_style")

        y_scrollbar = ttk.Scrollbar(table_frame, orient="vertical")
        y_scrollbar.pack(side="right", fill="y")

        x_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal")
        x_scrollbar.pack(side="bottom", fill="x")

        self.players_tree = ttk.Treeview(table_frame, columns=player_columns, show="headings",
                                 height=10, yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        self.players_tree.pack(side="right", fill="both", expand=True)

        x_scrollbar.config(command=self.players_tree.xview)
        y_scrollbar.config(command=self.players_tree.yview)

        self.players_tree.heading("player_id", text="ID")
        self.players_tree.heading("player_name", text="Player Name")
        self.players_tree.heading("player_role", text="Player Role")
        self.players_tree.heading("batting_style", text="Batting Style")
        self.players_tree.heading("bowling_style", text="Bowling Style")

        self.players_tree.column("player_id", width=190, anchor="center")
        self.players_tree.column("player_name", width=200, anchor="center")
        self.players_tree.column("player_role", width=100, anchor="center")
        self.players_tree.column("batting_style", width=100, anchor="center")
        self.players_tree.column("bowling_style", width=120, anchor="center")

        add_player_btn = tk.Button(right_frame, text="ADD PLAYER", width=15, command=self.add_player_to_team)
        add_player_btn.pack(side="right", padx=10, pady=10)

        remove_player_btn = tk.Button(right_frame, text="REMOVE PLAYER", width=15, command=self.remove_player_from_team)
        remove_player_btn.pack(side="left", padx=10, pady=10)

        self.search_player()

    def clear_tree(self):
        for item in self.players_tree.get_children():
            self.players_tree.delete(item)

    def search_player(self):
        self.clear_tree() #Removes all existing rows on tree
        term = self.search_var.get() #reads text entered in search box
        players = self.player_db.search_player(self.current_user, term) #Calls database function passing parameters

        for player in players:
            self.players_tree.insert(
                "", #"" = insert at root level, not nested
                "end", # adds row to bottom of the table
                values=(
                    str(player.get("_id", "")), # Mongo's primary key ObjectId enters GUI and replaces treeview_id
                    player.get("first_name") + " " + player.get("last_name"),
                    PlayerRole.get_value(player.get("player_role", "")),
                    BattingStyle.get_value(player.get("batting_style", "")),
                    BowlingStyle.get_value(player.get("bowling_style", "")), #index 7
                )
            )

    def refresh_leadership_dropdowns(self):
        options = [] #builds fresh list of dropdown options from current team
        self.name_to_player_id.clear()

        for player_id in self.team_tree.get_children(): #returns iids of team tree items
            row = self.team_tree.item(player_id, "values") #(position, player_name)
            player_name = row[1]
            display = f"{player_name}" #what the user sees in the dropdown
            options.append(display)
            self.name_to_player_id[display] = player_id #translates dropdown player_name to player_id

        #updates combobox options
        self.captain_dropdown["values"] = options
        self.wk_dropdown["values"] = options

        #clears invalid captains & wks that are no longer in selected team
        if self.captain_var.get() not in options:
            self.captain_var.set("")
        if self.wk_var.get() not in options:
            self.wk_var.set("")


    def add_player_to_team(self):
        selected = self.players_tree.selection()
        if not selected:
            return

        tree_iid = selected[0] #treeview iid
        values = self.players_tree.item(tree_iid, "values")

        mongo_player_id = str(values[0])
        player_name = values[1]

        if mongo_player_id in self.team_tree.get_children():
            messagebox.showerror("ERROR", "PLAYER ALREADY IN TEAM")
            return

        if len(self.team_tree.get_children()) >=11:
            messagebox.showerror("ERROR", "TEAM IS FULL")
            return

        next_position = None
        used_positions = {
            int(self.team_tree.item(i, "values")[0])
            for i in self.team_tree.get_children()
        }
        for position in range(1, 12):
            if position not in used_positions:
                next_position = position
                break

        self.team_tree.insert(
            "",
            "end",
            iid = mongo_player_id,
            values=(next_position, player_name, "", "",)
        )

        self.refresh_leadership_dropdowns()

    def remove_player_from_team(self):
        selected = self.team_tree.selection()
        if not selected:
            return
        self.team_tree.delete(selected[0])

        self.refresh_leadership_dropdowns()

    def clear_team(self):
        self.team_tree.delete(*self.team_tree.get_children())
        self.captain_var.set("")
        self.wk_var.set("")
        self.refresh_leadership_dropdowns()

    def save_team_and_continue(self):
        team_ids = list(self.team_tree.get_children())

        if len(team_ids) != 11:
            messagebox.showerror("ERROR", "SELECT EXACTLY 11 PLAYERS")
            return

        captain_id = self.name_to_player_id.get(self.captain_var.get(), "")
        wk_id= self.name_to_player_id.get(self.wk_var.get(), "")

        if not captain_id:
            messagebox.showerror("ERROR", "SELECT A CAPTAIN")
            return

        if not wk_id:
            messagebox.showerror("ERROR", "SELECT A WICKET-KEEPER")
            return

        if not captain_id in team_ids:
            messagebox.showerror("ERROR", "CAPTAIN MUST BE IN SELECTED TEAM")

        if not wk_id in team_ids:
            messagebox.showerror("ERROR", "WICKET-KEEPER MUST BE IN SELECTED TEAM")

        team_data = {
            "selected_team": team_ids,
            "captain_id": captain_id,
            "wk_id": wk_id
        }

        #print(team_data)

        match_id = self.match_id
        updated_match = self.match_db.update_match(self.current_user, match_id, team_data)

        if not updated_match:
            messagebox.showerror("ERROR", "TEAM SELECTION FAILED")

        messagebox.showinfo("SUCCESS", "TEAM SELECTION SUCCESSFUL")
        self.window.withdraw()
        MatchScorecard(tk.Toplevel(self.window), self.window, self.current_user, match_id, team_data)


    def go_back(self):
        self.window.destroy()
        self.parent.deiconify()



class MatchScorecard(BaseWindow):
    def __init__(self, window, parent, username, match_id, team_data):
        super().__init__(window)
        self.window = window
        self.parent = parent
        self.current_user = username
        self.match_id = match_id
        self.selected_team = team_data
        self.match_db = MatchDB()
        self.player_db = PlayerDB()
        self.all_players = self.player_db.get_all_players(username)
        self.window.title("SS - MATCH MANAGEMENT")
        self.center_window(1100, 900)

        self.batting_scorecard = {}
        self.bowling_scorecard = {}
        self.fielding_scorecard = {}

        self.create_widgets()


    def create_widgets(self):

        main_frame = self.create_main_frame()

        canvas = Canvas(main_frame)
        canvas.pack(side="left", fill="both", expand=1)

        self.create_header(canvas, "MATCH SCORECARD")

        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        self.create_sub_header(canvas, "BATTING SCORECARD")
        self.create_sub_header(canvas, "BOWLING SCORECARD")
        self.create_sub_header(canvas, "FIELDING SCORECARD")

        footer = tk.Frame(canvas)
        footer.pack(fill="x", side="bottom")

        back_btn = self.create_back_btn(footer, self.go_back)
        back_btn.pack(side="left", padx=10, pady=10)


    def go_back(self):
        self.window.destroy()
        self.parent.deiconify()






