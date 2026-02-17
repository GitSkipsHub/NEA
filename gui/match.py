import tkinter as tk
from tkinter import ttk, messagebox, Canvas
from datetime import datetime
from gui.baseWindow import BaseWindow
from bff.database import MatchDB, PlayerDB
from bff.enums import PlayerRole, BowlingStyle, BattingStyle, MatchFormat, Venue, Result, MatchType, HowOut, TossResult


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
                  command=self.open_update_match_page,
                  ).pack(pady=30)

        tk.Button(main_frame,
                  text="DELETE MATCH",
                  width=15,
                  height=3,
                  command=self.open_delete_match_page
                  ).pack(pady=40)

    def open_create_match_details_page(self):
        self.window.withdraw()
        CreateMatchDetailsPage(tk.Toplevel(self.window), self.window, self.current_user)

    def open_update_match_page(self):
        self.window.withdraw()
        UpdateMatchPage(tk.Toplevel(self.window), self.window, self.current_user)

    def open_delete_match_page(self):
        self.window.withdraw()
        DeleteMatchPage(tk.Toplevel(self.window), self.window, self.current_user)

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
        self.center_window(850,750)

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

        self.toss_result_var = tk.StringVar()
        self.create_dropdown(
            parent=form,
            text="TOSS RESULT: ",
            variable=self.toss_result_var,
            values=TossResult.list_values(),
            row=3
        )

        self.result_var = tk.StringVar()
        self.create_dropdown(
            parent=form,
            text="RESULT: ",
            variable=self.result_var,
            values=Result.list_values(),
            row=4
        )

        tk.Label(form, text="GROUND NAME: ").grid(column=0, row=5, pady=10, sticky="e")
        self.ground_name_input = tk.Entry(form)
        self.ground_name_input.configure(highlightthickness=3, highlightbackground="dodger blue")
        self.ground_name_input.grid(column=1, row=5, pady=10)

        tk.Label(form, text="OPPOSITION: ").grid(column=0, row=6, pady=10, sticky="e")
        self.opposition_input = tk.Entry(form)
        self.opposition_input.configure(highlightthickness=3, highlightbackground="dodger blue")
        self.opposition_input.grid(column=1, row=6, pady=10)

        tk.Label(form, text="DATE (YYYY-MM-DD): ").grid(column=0, row=7, pady=10, sticky="e")
        self.date_input = tk.Entry(form)
        self.date_input.configure(highlightthickness=3, highlightbackground="dodger blue")
        self.date_input.grid(column=1, row=7, pady=10)


        footer = tk.Frame(main_frame)
        footer.pack(fill="x", side="bottom")

        save_btn = tk.Button(footer, text="SAVE", command=self.save_match_details_and_continue, width=15)
        save_btn.pack(side="right", padx=20, pady=20)

        back_btn = self.create_back_btn(footer, self.go_back)
        back_btn.pack(side="left", padx=20, pady=20)

        cancel_btn = tk.Button(footer, text="CANCEL", command=self.cancel_match_creation, width=15)
        cancel_btn.pack(side="bottom", padx=10, pady=10)

    def cancel_match_creation(self):
        if not messagebox.askyesno("CANCEL MATCH CREATION","ARE YOU SURE YOU WANT TO DELETE THIS MATCH RECORD?"):
            return

        deleted = self.match_db.delete_match(self.current_user, self.created_match_id)

        if not deleted:
            messagebox.showerror("ERROR", "Could not delete match record (maybe already deleted).")
            return

        self.window.withdraw()
        MatchManagementPage(tk.Toplevel(self.window), self.window, self.current_user)


    def save_match_details_and_continue(self):

        #Strips all inputs
        match_type_value = self.match_type_var.get().strip()
        match_format_value = self.match_format_var.get().strip()
        venue_value = self.venue_var.get().strip()
        result_value = self.result_var.get().strip()
        toss_result_value = self.toss_result_var.get().strip()
        ground_name = self.ground_name_input.get().strip()
        opposition = self.opposition_input.get().strip()
        match_date = self.date_input.get().strip()

        if (not match_type_value or not match_format_value or not venue_value or not result_value or not toss_result_value
                or not ground_name or not opposition or not match_date):
                messagebox.showerror("Error", "Please fill in all required fields")
                return

        #Datetime validation
        try:
            datetime.strptime(match_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("ERROR", "Date must be in YYYY-MM-DD format (e.g., 2007-04-19)")
            return

        match_data = {
            "match_type": MatchType.get_key(match_type_value), #stores enum key into mongo
            "match_format": MatchFormat.get_key(match_format_value),
            "venue": Venue.get_key(venue_value),
            "result": Result.get_key(result_value),
            "toss_result": TossResult.get_key(toss_result_value),
            "ground_name": ground_name,
            "opposition": opposition,
            "match_date": match_date,
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

        cancel_btn = tk.Button(footer, text="CANCEL", command=self.cancel_match, width=15)
        cancel_btn.pack(side="bottom", padx=10, pady=10)

        content_frame = tk.Frame(main_frame, highlightbackground="dodger blue", highlightthickness=4)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        left_frame = tk.Frame(content_frame, highlightbackground="white", highlightthickness=2, width=700)
        left_frame.pack(side="left", fill="y", padx=10, pady=10)
        left_frame.pack_propagate(False)

        clear_btn = tk.Button(left_frame, text="CLEAR TEAM", width=15, command=self.clear_team)
        clear_btn.pack(side="bottom", padx=20, pady=20)

        team_frame = tk.Frame(left_frame)
        team_frame.pack(fill="both", expand=True, padx=20, pady=10)

        x_scrollbar = ttk.Scrollbar(team_frame, orient="horizontal")
        x_scrollbar.pack(side="bottom", fill="x")

        team_columns = ("position", "player_name", "player_role", "batting_style", "bowling_style")

        self.team_tree = ttk.Treeview(team_frame, columns=team_columns, show="headings", height=12,
                                      xscrollcommand=x_scrollbar.set)
        self.team_tree.pack(side="right", fill="both", expand=True)
        x_scrollbar.config(command=self.team_tree.xview)


        self.team_tree.heading("position", text="POS")
        self.team_tree.heading("player_name", text="Player Name")
        self.team_tree.heading("player_role", text="Player Role")
        self.team_tree.heading("batting_style", text="Batting Style")
        self.team_tree.heading("bowling_style", text="Bowling Style")

        self.team_tree.column("position", width=50, anchor="center")
        self.team_tree.column("player_name", width=200, anchor="center")
        self.team_tree.column("player_role", width=200, anchor="center")
        self.team_tree.column("batting_style", width=200, anchor="center")
        self.team_tree.column("bowling_style", width=200, anchor="center")

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
        self.players_tree.column("bowling_style", width=150, anchor="center")

        add_player_btn = tk.Button(right_frame, text="ADD PLAYER", width=15, command=self.add_player_to_team)
        add_player_btn.pack(side="right", padx=10, pady=10)

        remove_player_btn = tk.Button(right_frame, text="REMOVE PLAYER", width=15, command=self.remove_player_from_team)
        remove_player_btn.pack(side="left", padx=10, pady=10)

        self.search_player()

    def cancel_match(self):
        if not messagebox.askyesno("CANCEL MATCH CREATION","ARE YOU SURE YOU WANT TO DELETE THIS MATCH RECORD?"):
            return

        deleted = self.match_db.delete_match(self.current_user, self.match_id)

        if not deleted:
            messagebox.showerror("ERROR", "Could not delete match record (maybe already deleted).")
            return

        self.window.withdraw()
        MatchManagementPage(tk.Toplevel(self.window), self.window, self.current_user)

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
        self.name_to_player_id.clear() #empties the lookup dictionary

        for player_id in self.team_tree.get_children(): #returns iids of team tree items
            row = self.team_tree.item(player_id, "values") #returns row's stored values(position, player_name)
            player_name = row[1] #assigns variable player_name to tuple index 1
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
        selected = self.players_tree.selection() #returns iid of selected player
        if not selected:
            return

        tree_iid = selected[0] #takes first selected row tree_iid
        values = self.players_tree.item(tree_iid, "values") #return values stored in that row tree_iid

        mongo_player_id = str(values[0])
        player_name = values[1]
        player_role = values[2]
        batting_style = values[3]
        bowling_style = values[4]

        if mongo_player_id in self.team_tree.get_children():
            messagebox.showerror("ERROR", "PLAYER ALREADY IN TEAM")
            return

        if len(self.team_tree.get_children()) >=11:
            messagebox.showerror("ERROR", "TEAM IS FULL")
            return

        next_position = None
        used_positions = set() #data structure where number can only appear once
        for i in self.team_tree.get_children():
            values = self.team_tree.item(i, "values")
            pos = int(values[0])
            used_positions.add(pos)

        for position in range(1, 12):
            if position not in used_positions:
                next_position = position
                break

        self.team_tree.insert(
            "",
            "end",
            iid = mongo_player_id,
            values=(next_position, player_name, player_role, batting_style, bowling_style)
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
            return

        if not wk_id in team_ids:
            messagebox.showerror("ERROR", "WICKET-KEEPER MUST BE IN SELECTED TEAM")
            return

        team_players = []
        for player_id in team_ids:
            pos, player_name, player_role, batting_style, bowling_style = self.team_tree.item(player_id, "values")
            team_players.append({
                "player_id": player_id,
                "position": int(pos),
                "player_name": player_name,
                "player_role": PlayerRole.get_key(player_role),
                "batting_style": BattingStyle.get_key(batting_style),
                "bowling_style": BowlingStyle.get_key(bowling_style)
            })

        team_players.sort(key=lambda p: p["position"])

        selected_team = {
            "team_players": team_players,
            "captain_id": captain_id,
            "wk_id": wk_id
        }

        #print(team_data)

        match_id = self.match_id
        updated_match = self.match_db.update_match(self.current_user, match_id, selected_team)

        if not updated_match:
            messagebox.showerror("ERROR", "TEAM SELECTION FAILED")

        else:
            messagebox.showinfo("SUCCESS", "TEAM SELECTION SUCCESSFUL")

        self.window.withdraw()
        MatchScorecard(tk.Toplevel(self.window), self.window, self.current_user, match_id, selected_team)

    def go_back(self):
        self.window.destroy()
        self.parent.deiconify()



class MatchScorecard(BaseWindow):
    def __init__(self, window, parent, username, match_id, selected_team):
        super().__init__(window)
        self.window = window
        self.parent = parent
        self.current_user = username
        self.match_id = match_id
        self.selected_team = selected_team
        self.match_db = MatchDB()
        self.player_db = PlayerDB()
        self.all_players = self.player_db.get_all_players(username)
        self.window.title("SS - MATCH MANAGEMENT")
        self.center_window(1400, 900)

        # self.batting_scorecard = [] #list[dict]
        # self.bowling_scorecard = [] #list[dict]
        # self.fielding_scorecard = [] #list[dict]

        self.batting_entries = [] #list[dict]
        self.bowling_entries = [] #list[dict]
        self.fielding_entries = [] #list[dict]

        self.create_widgets()

    def create_widgets(self):

        main_frame = self.create_main_frame()

        footer = tk.Frame(main_frame)
        footer.pack(fill="x", side="bottom")

        back_btn = self.create_back_btn(footer, self.go_back)
        back_btn.pack(side="left", padx=10, pady=10)

        save_scorecard_btn = tk.Button(footer,  text="SAVE SCORECARDS", width=15, command=self.save_scorecards)
        save_scorecard_btn.pack(side="right", padx=20, pady=20)

        cancel_btn = tk.Button(footer, text="CANCEL", command=self.cancel_match, width=15)
        cancel_btn.pack(side="bottom", padx=10, pady=10)

        canvas = Canvas(main_frame)
        canvas.pack(side="left", fill="both", expand=True)

        y_scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        y_scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=y_scrollbar.set)

        content_frame = tk.Frame(canvas)
        canvas_window = canvas.create_window((0, 0), window=content_frame, anchor="nw")

        content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))) #recalculates scrollable area
        canvas.bind("<Configure>", lambda e: canvas.itemconfigure(canvas_window, width=e.width)) #centers content

        self.create_header(content_frame,  "MATCH SCORECARD")


        #--------------------------------------------BATTING SCORECARD-------------------------------------------------#


        self.create_sub_header(content_frame, "BATTING SCORECARD")

        batting_table = tk.Frame(content_frame)
        batting_table.pack(padx=20, pady=20, anchor="center")

        bat_headers = ["POS", "PLAYER", "HOW OUT", "FIELDER", "BOWLER", "RUNS", "BALLS", "4s", "6s"]

        for column_index, header_text in enumerate(bat_headers):
            tk.Label(batting_table,text=header_text, font=("Arial", 11, "bold")).grid(row=0, column=column_index, padx=10, pady=6)

        team_players = self.selected_team["team_players"]
        self.batting_entries.clear()

        for index, player in enumerate(team_players):
            r = index + 1

            row = {
                "player_id": tk.StringVar(value=str(player["player_id"])),
                "position": tk.StringVar(value=str(player["position"])),
                "player_name": tk.StringVar(value=str(player["player_name"])),
                "player_role": tk.StringVar(value=str(player.get("player_role", ""))),
                "batting_style": tk.StringVar(value=str(player.get("batting_style", ""))),

                "how_out": tk.StringVar(value="NOT OUT"),
                "fielder": tk.StringVar(value=""),
                "bowler": tk.StringVar(value=""),

                "runs_scored": tk.StringVar(value="0"),
                "balls": tk.StringVar(value="0"),
                "fours": tk.StringVar(value="0"),
                "sixes": tk.StringVar(value="0"),
            }

            self.batting_entries.append(row)

            position = (tk.Label(batting_table, textvariable=row["position"], width=4, anchor="center"))
            position.grid(row=r, column=0, padx=4, pady=3)
            position.configure(background="dodger blue")


            player_name = (tk.Label(batting_table, textvariable=row["player_name"], width=20, anchor="center",))
            player_name.grid(row=r, column=1,padx=4, pady=3)
            player_name.configure(background="dodger blue")


            ttk.Combobox(
                batting_table,
                textvariable=row["how_out"],
                values= HowOut.list_values(),
                state="readonly",
                width=12
            ).grid(row=r, column=2, padx=4, pady=3)

            fielder_entry = (tk.Entry(batting_table, textvariable=row["fielder"], width=15))
            fielder_entry.grid(row=r, column=3, padx=4, pady=3)
            fielder_entry.configure(highlightbackground="dodger blue", highlightthickness=2.5)

            bowler_entry = (tk.Entry(batting_table, textvariable=row["bowler"], width=15))
            bowler_entry.grid(row=r, column=4, padx=4, pady=3)
            bowler_entry.configure(highlightbackground="dodger blue", highlightthickness=2.5)

            runs_entry = (tk.Entry(batting_table, textvariable=row["runs_scored"], width=5))
            runs_entry.grid(row=r, column=5, padx=4, pady=3)
            runs_entry.configure(highlightbackground="dodger blue", highlightthickness=2.5)

            balls_entry = tk.Entry(batting_table, textvariable=row["balls"], width=5)
            balls_entry.grid(row=r, column=6, padx=4, pady=3)
            balls_entry.configure(highlightbackground="dodger blue", highlightthickness=2.5)

            fours_entry = (tk.Entry(batting_table, textvariable=row["fours"], width=5))
            fours_entry.grid(row=r, column=7, padx=4, pady=3)
            fours_entry.configure(highlightbackground="dodger blue", highlightthickness=2.5)

            sixes_entry = (tk.Entry(batting_table, textvariable=row["sixes"], width=5))
            sixes_entry.grid(row=r, column=8, padx=4, pady=3)
            sixes_entry.configure(highlightbackground="dodger blue", highlightthickness=2.5)

        self.total_var = tk.StringVar(batting_table, value="0")
        self.extras_var = tk.StringVar(batting_table, value="0")
        self.subtotal_var = tk.StringVar(batting_table, value="0")

        totals_row = len(team_players) + 1

        tk.Label(batting_table, text="SUBTOTAL : ", font=("Arial", 11, "bold")).grid(row=totals_row, column=1, padx=10,pady=35, sticky="e")
        subtotal_entry = tk.Entry(batting_table, textvariable=self.subtotal_var, width=5)
        subtotal_entry.grid(row=totals_row, column=2, padx=4, pady=35)
        subtotal_entry.configure(highlightthickness=2.5, highlightbackground="dodger blue")

        tk.Label(batting_table, text="EXTRAS : ", font=("Arial", 11, "bold")).grid( row=totals_row, column=3, padx=10, pady=35, sticky="e")
        extras_entry = tk.Entry(batting_table, textvariable=self.extras_var, width=5)
        extras_entry.grid(row=totals_row, column=4, padx=4, pady=35)
        extras_entry.configure(highlightthickness=2.5, highlightbackground="dodger blue")

        tk.Label(batting_table, text="TOTAL : ", font=("Arial", 11, "bold")).grid(row=totals_row, column=5, padx=10, pady=35, sticky="e")
        total_entry = tk.Entry(batting_table, textvariable=self.total_var, width=5)
        total_entry.grid(row=totals_row, column=6, padx=4, pady=35)
        total_entry.configure(highlightthickness=2.5, highlightbackground="dodger blue")


        #--------------------------------------------BOWLING SCORECARD-------------------------------------------------#


        self.create_sub_header(content_frame, "BOWLING SCORECARD")

        bowling_table = tk.Frame(content_frame)
        bowling_table.pack(padx=20, pady=20, anchor="center")

        bowl_headers = ["POS", "PLAYER", "OVERS", "MAIDENS", "RUNS", "WICKETS", "WIDES", "NO BALLS"]

        for column_index, header_text in enumerate(bowl_headers):
            tk.Label(bowling_table,text=header_text, font=("Arial", 11, "bold")).grid(row=0, column=column_index,
                                                                                      padx=10, pady=6)

        team_players = self.selected_team["team_players"]
        self.bowling_entries.clear()

        for index, player in enumerate(team_players):
            r = index + 1

            row = {
                "player_id": tk.StringVar(value=str(player["player_id"])),
                "position": tk.StringVar(value=str(player["position"])),
                "player_name": tk.StringVar(value=str(player["player_name"])),
                "player_role": tk.StringVar(value=str(player.get("player_role", ""))),
                "bowling_style": tk.StringVar(value=str(player.get("bowling_style", ""))),
                "overs": tk.StringVar(value="0.0"),
                "maidens": tk.StringVar(value="0"),
                "runs_conceded": tk.StringVar(value="0"),
                "wickets": tk.StringVar(value="0"),
                "wides": tk.StringVar(value="0"),
                "no_balls": tk.StringVar(value="0")
            }

            self.bowling_entries.append(row)

            position = (tk.Label(bowling_table, textvariable=row["position"], width=4, anchor="center",))
            position.grid(row=r, column=0, padx=4, pady=3)
            position.configure(background="dodger blue")

            player_name = (tk.Label(bowling_table, textvariable=row["player_name"], width=20, anchor="center",))
            player_name.grid(row=r, column=1,padx=4, pady=3)
            player_name.configure(background="dodger blue")

            overs_entry = (tk.Entry(bowling_table, textvariable=row["overs"], width=5))
            overs_entry.grid(row=r, column=2, padx=4, pady=3)
            overs_entry.configure(highlightbackground="dodger blue", highlightthickness=2.5)

            maidens_entry = (tk.Entry(bowling_table, textvariable=row["maidens"], width=5))
            maidens_entry.grid(row=r, column=3, padx=4, pady=3)
            maidens_entry.configure(highlightbackground="dodger blue", highlightthickness=2.5)

            runs_entry = (tk.Entry(bowling_table, textvariable=row["runs_conceded"], width=5))
            runs_entry.grid(row=r, column=4, padx=4, pady=3)
            runs_entry.configure(highlightbackground="dodger blue", highlightthickness=2.5)

            wickets_entry = (tk.Entry(bowling_table, textvariable=row["wickets"], width=5))
            wickets_entry.grid(row=r, column=5, padx=4, pady=3)
            wickets_entry.configure(highlightbackground="dodger blue", highlightthickness=2.5)

            wides_entry = (tk.Entry(bowling_table, textvariable=row["wides"], width=5))
            wides_entry.grid(row=r, column=6, padx=4, pady=3)
            wides_entry.configure(highlightbackground="dodger blue", highlightthickness=2.5)

            no_balls_entry = (tk.Entry(bowling_table, textvariable=row["no_balls"], width=5))
            no_balls_entry.grid(row=r, column=7, padx=4, pady=3)
            no_balls_entry.configure(highlightbackground="dodger blue", highlightthickness=2.5)


        #--------------------------------------------FIELDING SCORECARD-------------------------------------------------#


        self.create_sub_header(content_frame, "FIELDING SCORECARD")

        fielding_table = tk.Frame(content_frame)
        fielding_table.pack(padx=20, pady=20, anchor="center")

        field_headers = ["POS", "PLAYER", "CATCHES", "RUNOUTS", "STUMPINGS"]

        for column_index, header_text in enumerate(field_headers):
            tk.Label(fielding_table ,text=header_text, font=("Arial", 11, "bold")).grid(row=0, column=column_index,
                                                                                      padx=10, pady=6)

        team_players = self.selected_team["team_players"]
        self.fielding_entries.clear()

        for index, player in enumerate(team_players):
            r = index + 1

            row = {
                "player_id": tk.StringVar(value=str(player["player_id"])),
                "position": tk.StringVar(value=str(player["position"])),
                "player_name": tk.StringVar(value=str(player["player_name"])),
                "player_role": tk.StringVar(value=str(player.get("player_role", ""))),
                "batting_style": tk.StringVar(value=str(player.get("batting_style", ""))),
                "catches": tk.StringVar(value="0"),
                "runouts": tk.StringVar(value="0"),
                "stumpings": tk.StringVar(value="0"),
            }

            self.fielding_entries.append(row)

            position = (tk.Label(fielding_table, textvariable=row["position"], width=4, anchor="center",))
            position.grid(row=r, column=0, padx=4, pady=3)
            position.configure(background="dodger blue")

            player_name = (tk.Label(fielding_table, textvariable=row["player_name"], width=20, anchor="center",))
            player_name.grid(row=r, column=1,padx=4, pady=3)
            player_name.configure(background="dodger blue")

            catches_entry = (tk.Entry(fielding_table, textvariable=row["catches"], width=5))
            catches_entry.grid(row=r, column=2, padx=4, pady=3)
            catches_entry.configure(highlightbackground="dodger blue", highlightthickness=2.5)

            runouts_entry = (tk.Entry(fielding_table, textvariable=row["runouts"], width=5))
            runouts_entry.grid(row=r, column=3, padx=4, pady=3)
            runouts_entry.configure(highlightbackground="dodger blue", highlightthickness=2.5)

            stumpings_entry = (tk.Entry(fielding_table, textvariable=row["stumpings"], width=5))
            stumpings_entry.grid(row=r, column=4, padx=4, pady=3)
            stumpings_entry.configure(highlightbackground="dodger blue", highlightthickness=2.5)

        self.byes = tk.StringVar(fielding_table, value="0")
        self.leg_byes = tk.StringVar(fielding_table, value="0")
        self.penalties = tk.StringVar(fielding_table, value="0")

        totals_row = len(team_players) + 1

        tk.Label(fielding_table, text="BYES : ", font=("Arial", 11, "bold")).grid(row=totals_row, column=0, padx=10,pady=35, sticky="e")
        subtotal_entry = tk.Entry(fielding_table, textvariable=self.byes, width=5)
        subtotal_entry.grid(row=totals_row, column=1, padx=4, pady=35)
        subtotal_entry.configure(highlightthickness=2.5, highlightbackground="dodger blue")

        tk.Label(fielding_table, text="LEG BYES : ", font=("Arial", 11, "bold")).grid( row=totals_row, column=2, padx=10, pady=35, sticky="e")
        extras_entry = tk.Entry(fielding_table, textvariable=self.leg_byes, width=5)
        extras_entry.grid(row=totals_row, column=3, padx=4, pady=35)
        extras_entry.configure(highlightthickness=2.5, highlightbackground="dodger blue")

        tk.Label(fielding_table, text="PENALTIES : ", font=("Arial", 11, "bold")).grid(row=totals_row, column=4, padx=10, pady=35, sticky="e")
        total_entry = tk.Entry(fielding_table, textvariable=self.penalties, width=5)
        total_entry.grid(row=totals_row, column=5, padx=4, pady=35)
        total_entry.configure(highlightthickness=2.5, highlightbackground="dodger blue")

    def cancel_match(self):
        if not messagebox.askyesno("CANCEL MATCH CREATION","ARE YOU SURE YOU WANT TO DELETE THIS MATCH RECORD?"):
            return

        deleted = self.match_db.delete_match(self.current_user, self.match_id)

        if not deleted:
            messagebox.showerror("ERROR", "Could not delete match record (maybe already deleted).")
            return

        self.window.withdraw()
        MatchManagementPage(tk.Toplevel(self.window), self.window, self.current_user)


    def save_scorecards(self):

        batting_data = []
        try:
            subtotal = int(self.subtotal_var.get())
            extras = int(self.extras_var.get())
            total = int(self.total_var.get())

        except ValueError:
            messagebox.showerror("ERROR", "VALUES MUST BE INTEGERS")
            return

        if min(subtotal, extras, total)<0:
            messagebox.showerror("ERROR", "VALUES CANNOT BE NEGATIVE")
            return

        if subtotal + extras != total:
            messagebox.showerror("ERROR", "TOTAL MUST EQUAL SUBTOTAL + EXTRAS.")
            return

        batting_summary = {
                "subtotal": subtotal,
                "extras": extras,
                "total": total
        }

        for row in self.batting_entries:
            try:
                runs_scored = int(row["runs_scored"].get())
                balls = int(row["balls"].get())
                fours = int(row["fours"].get())
                sixes = int(row["sixes"].get())

            except ValueError:
                messagebox.showerror("ERROR", "STATS MUST BE INTEGERS")
                return

            if min(runs_scored, balls, fours, sixes)<0:
                messagebox.showerror("ERROR", "VALUES CANNOT BE NEGATIVE")
                return

            batting_data.append({
                "player_id": row["player_id"].get(),
                "position": row["position"].get(),
                "player_name": row["player_name"].get(),
                "player_role": row["player_role"].get(),
                "batting_style": row["batting_style"].get(),
                "how_out": row["how_out"].get(),
                "fielder": row["fielder"].get(),
                "bowler": row["bowler"].get(),
                "runs_scored": runs_scored,
                "balls": balls,
                "fours": fours,
                "sixes": sixes,
            })


        bowling_data = []
        for row in self.bowling_entries:
            try:
                overs = float(row["overs"].get())
                maidens = int(row["maidens"].get())
                runs_conceded = int(row["runs_conceded"].get())
                wickets = int(row["wickets"].get())
                wides = int(row["wides"].get())
                no_balls = int(row["no_balls"].get())

            except ValueError:
                messagebox.showerror("ERROR", "ALL STATS (EXCEPT OVERS) MUST BE INTEGERS")
                return

            if min(overs, maidens, runs_conceded, wickets, wides, no_balls) <0:
                messagebox.showerror("ERROR", "VALUES CANNOT BE NEGATIVE")
                return

            if overs %1 >=0.6:
                messagebox.showerror("ERROR", "OVERS MUST HAVE .0 to .5 ONLY")
                return

            bowling_data.append({
                "player_id": row["player_id"].get(),
                "position": row["position"].get(),
                "player_name": row["player_name"].get(),
                "player_role": row["player_role"].get(),
                "bowling_style": row["bowling_style"].get(),
                "overs": overs,
                "maidens": maidens,
                "runs_conceded": runs_conceded,
                "wickets": wickets,
                "wides": wides,
                "no_balls": no_balls,
            })


        fielding_data = []

        try:
            byes = int(self.byes.get())
            leg_byes = int(self.leg_byes.get())
            penalties = int(self.penalties.get())

        except ValueError:
            messagebox.showerror("ERROR", "VALUES MUST BE INTEGERS")
            return

        if min(byes, leg_byes, penalties)<0:
            messagebox.showerror("ERROR", "VALUES CANNOT BE NEGATIVE")
            return

        fielding_extras = {
            "byes": byes,
            "leg_byes": leg_byes,
            "penalties": penalties
        }

        for row in self.fielding_entries:
            try:
                catches = int(row["catches"].get())
                runouts = int(row["runouts"].get())
                stumpings = int(row["stumpings"].get())

            except ValueError:
                messagebox.showerror("ERROR", "STATS MUST BE INTEGERS")
                return

            if min(catches, runouts, stumpings)<0:
                messagebox.showerror("ERROR", "VALUES CANNOT BE NEGATIVE")
                return

            fielding_data.append({
                "player_id": row["player_id"].get(),
                "position": row["position"].get(),
                "player_name": row["player_name"].get(),
                "player_role": row["player_role"].get(),
                "batting_style": row["batting_style"].get(),
                "catches": catches,
                "runouts": runouts,
                "stumpings": stumpings
            })

        scorecard_data = self.match_db.update_match(self.current_user, self.match_id, {"batting_scorecard": batting_data,
                                                                                       "batting_summary": batting_summary,
                                                                                       "bowling_scorecard": bowling_data,
                                                                                     "fielding_scorecard": fielding_data,
                                                                                       "fielding_extras": fielding_extras})

        if scorecard_data:
            messagebox.showinfo("SUCCESS", "ALL SCORECARDS SAVED")
            self.window.withdraw()
            MatchManagementPage(tk.Toplevel(self.window), self.window, self.current_user)

        else:
            messagebox.showerror("ERROR", "FAILED TO SAVE SCORECARD")


    def go_back(self):
        self.window.destroy()
        self.parent.deiconify()


class UpdateMatchPage(BaseWindow):
    def __init__(self, window, parent, username):
        super().__init__(window)
        self.window = window
        self.parent = parent
        self.current_user = username

        self.match_db = MatchDB()
        self.selected_match_id = None

        self.window.title("SS - UPDATE MATCH")
        self.center_window(1250, 700)

        self.create_widgets()

    def create_widgets(self):
        main_frame = self.create_main_frame()
        self.create_header(main_frame, "UPDATE MATCH")
        self.create_sub_header(main_frame, "SELECT A MATCH")

        # Footer
        footer = tk.Frame(main_frame)
        footer.pack(fill="x", side="bottom")

        back_btn = self.create_back_btn(footer, self.go_back)
        back_btn.pack(side=tk.LEFT, padx=20, pady=20)

        btn_frame = tk.Frame(footer)
        btn_frame.pack(side="right", padx=20, pady=20)

        tk.Button(btn_frame, text="EDIT DETAILS", width=15, command=self.open_edit_details).pack(side="left", padx=6)

        # Search (simple: opposition)
        search_frame = tk.Frame(main_frame)
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="SEARCH OPPOSITION: ").grid(row=0, column=0, padx=8, pady=8, sticky="e")
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.configure(highlightthickness=3, highlightbackground="dodger blue")
        search_entry.grid(row=0, column=1, padx=8, pady=8)

        tk.Button(search_frame, text="SEARCH", width=12, command=self.load_matches).grid(row=0, column=2, padx=10)

        # Matches table
        table_frame = tk.Frame(main_frame)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        cols = ("match_id", "match_date", "opposition", "venue", "match_type", "match_format", "result")
        y_scroll = ttk.Scrollbar(table_frame, orient="vertical")
        y_scroll.pack(side="right", fill="y")

        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", yscrollcommand=y_scroll.set, height=14)
        self.tree.pack(fill="both", expand=True)
        y_scroll.config(command=self.tree.yview)

        self.tree.heading("match_id", text="MATCH ID")
        self.tree.heading("match_date", text="DATE")
        self.tree.heading("opposition", text="OPPOSITION")
        self.tree.heading("venue", text="VENUE")
        self.tree.heading("match_type", text="TYPE")
        self.tree.heading("match_format", text="FORMAT")
        self.tree.heading("result", text="RESULT")

        self.tree.column("match_id", width=230, anchor="center")
        self.tree.column("match_date", width=110, anchor="center")
        self.tree.column("opposition", width=200, anchor="center")
        self.tree.column("venue", width=90, anchor="center")
        self.tree.column("match_type", width=120, anchor="center")
        self.tree.column("match_format", width=120, anchor="center")
        self.tree.column("result", width=110, anchor="center")

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        self.load_matches()

    def clear_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def load_matches(self):
        self.clear_tree()

        filters = {}
        term = self.search_var.get().strip()
        if term:
            filters["opposition"] = term

        matches = self.match_db.search_match(self.current_user, filters)

        for m in matches:
            match_id = str(m.get("_id", ""))
            self.tree.insert(
                "",
                "end",
                iid=match_id,
                values=(
                    match_id,
                    m.get("match_date", ""),
                    m.get("opposition", ""),
                    Venue.get_value(m.get("venue", "")),
                    MatchType.get_value(m.get("match_type", "")),
                    MatchFormat.get_value(m.get("match_format", "")),
                    Result.get_value(m.get("result", ""))
                )
            )

        self.selected_match_id = None

    def on_select(self, event=None):
        selected = self.tree.selection()
        if not selected:
            self.selected_match_id = None
            return
        self.selected_match_id = selected[0]

    def require_selected(self) -> bool:
        if not self.selected_match_id:
            messagebox.showerror("ERROR", "SELECT A MATCH FIRST")
            return False
        return True

    def open_edit_details(self):
        if not self.require_selected():
            return
        self.window.withdraw()
        EditMatchDetailsPage(tk.Toplevel(self.window), self.window, self.current_user, self.selected_match_id)

    def go_back(self):
        self.window.destroy()
        self.parent.deiconify()


class EditMatchDetailsPage(BaseWindow):
    def __init__(self, window, parent, username, match_id):
        super().__init__(window)
        self.window = window
        self.parent = parent
        self.current_user = username
        self.match_id = match_id
        self.match_db = MatchDB()

        self.window.title("SS - EDIT MATCH DETAILS")
        self.center_window(850, 650)

        self.match_doc = self.match_db.find_match(self.current_user, self.match_id)
        if not self.match_doc:
            messagebox.showerror("ERROR", "MATCH NOT FOUND")
            self.window.destroy()
            self.parent.deiconify()
            return

        self.create_widgets()

    def create_widgets(self):
        main_frame = self.create_main_frame()
        self.create_header(main_frame, "UPDATE MATCH")
        self.create_sub_header(main_frame, "EDIT DETAILS")

        form = tk.Frame(main_frame)
        form.pack(pady=10)

        self.match_type_var = tk.StringVar(value=MatchType.get_value(self.match_doc.get("match_type", "")))
        self.create_dropdown(form, "MATCH TYPE: ", self.match_type_var, MatchType.list_values(), row=0)

        self.match_format_var = tk.StringVar(value=MatchFormat.get_value(self.match_doc.get("match_format", "")))
        self.create_dropdown(form, "MATCH FORMAT: ", self.match_format_var, MatchFormat.list_values(), row=1)

        self.venue_var = tk.StringVar(value=Venue.get_value(self.match_doc.get("venue", "")))
        self.create_dropdown(form, "VENUE: ", self.venue_var, Venue.list_values(), row=2)

        self.result_var = tk.StringVar(value=self.match_doc.get("result", ""))
        self.create_dropdown(form, "RESULT: ", self.result_var, Result.list_values(), row=3)

        tk.Label(form, text="GROUND NAME: ").grid(column=0, row=4, pady=10, sticky="e")
        self.ground_input = tk.Entry(form, width=30)
        self.ground_input.configure(highlightthickness=3, highlightbackground="dodger blue")
        self.ground_input.grid(column=1, row=4, pady=10)
        self.ground_input.insert(0, self.match_doc.get("ground_name", ""))

        tk.Label(form, text="OPPOSITION: ").grid(column=0, row=5, pady=10, sticky="e")
        self.opp_input = tk.Entry(form, width=30)
        self.opp_input.configure(highlightthickness=3, highlightbackground="dodger blue")
        self.opp_input.grid(column=1, row=5, pady=10)
        self.opp_input.insert(0, self.match_doc.get("opposition", ""))

        tk.Label(form, text="DATE (YYYY-MM-DD): ").grid(column=0, row=6, pady=10, sticky="e")
        self.date_input = tk.Entry(form, width=30)
        self.date_input.configure(highlightthickness=3, highlightbackground="dodger blue")
        self.date_input.grid(column=1, row=6, pady=10)
        self.date_input.insert(0, self.match_doc.get("match_date", ""))

        footer = tk.Frame(main_frame)
        footer.pack(fill="x", side="bottom")

        save_btn = tk.Button(footer, text="SAVE", width=15, command=self.save_changes)
        save_btn.pack(side="right", padx=20, pady=20)

        back_btn = self.create_back_btn(footer, self.go_back)
        back_btn.pack(side=tk.LEFT, padx=20, pady=20)

    def save_changes(self):
        match_type_value = self.match_type_var.get().strip()
        match_format_value = self.match_format_var.get().strip()
        venue_value = self.venue_var.get().strip()
        result_value = self.result_var.get().strip()
        ground_name = self.ground_input.get().strip()
        opposition = self.opp_input.get().strip()
        match_date = self.date_input.get().strip()

        if (not match_type_value or not match_format_value or not venue_value or not result_value
                or not ground_name or not opposition or not match_date):
            messagebox.showerror("ERROR", "FILL IN ALL FIELDS")
            return

        try:
            datetime.strptime(match_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("ERROR", "DATE MUST BE YYYY-MM-DD")
            return

        update_data = {
            "match_type": MatchType.get_key(match_type_value),
            "match_format": MatchFormat.get_key(match_format_value),
            "venue": Venue.get_key(venue_value),
            "result": result_value,
            "ground_name": ground_name,
            "opposition": opposition,
            "match_date": match_date
        }

        ok = self.match_db.update_match(self.current_user, self.match_id, update_data)
        if not ok:
            messagebox.showerror("ERROR", "UPDATE FAILED")
            return

        messagebox.showinfo("SUCCESS", "MATCH UPDATED")
        self.go_back()

    def go_back(self):
        self.window.destroy()
        self.parent.deiconify()


class DeleteMatchPage(BaseWindow):
    def __init__(self, window, parent, username):
        super().__init__(window)
        self.window = window
        self.parent = parent
        self.current_user = username
        self.match_db = MatchDB()

        self.window.title("SS - DELETE MATCH")
        self.center_window(1100, 750)

        self.create_widgets()

    def create_widgets(self):
        main_frame = self.create_main_frame()
        self.create_header(main_frame, "DELETE MATCH")
        self.create_sub_header(main_frame, "SELECT A MATCH")

        footer = tk.Frame(main_frame)
        footer.pack(fill="x", side="bottom")

        back_btn = self.create_back_btn(footer, self.go_back)
        back_btn.pack(side=tk.LEFT, padx=20, pady=20)

        delete_btn = tk.Button(footer, text="DELETE", width=15, command=self.delete_match)
        delete_btn.pack(side="right", padx=20, pady=20)

        # small search box (optional)
        search_frame = tk.Frame(main_frame)
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="SEARCH OPPOSITION: ").grid(row=0, column=0, padx=8, pady=8, sticky="e")
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.configure(highlightthickness=3, highlightbackground="dodger blue")
        search_entry.grid(row=0, column=1, padx=8, pady=8)

        tk.Button(search_frame, text="SEARCH", width=12, command=self.load_matches).grid(row=0, column=2, padx=10)

        table_frame = tk.Frame(main_frame)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        cols = ("match_id", "date", "opposition", "venue")
        y_scroll = ttk.Scrollbar(table_frame, orient="vertical")
        y_scroll.pack(side="right", fill="y")

        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", yscrollcommand=y_scroll.set, height=12)
        self.tree.pack(fill="both", expand=True)
        y_scroll.config(command=self.tree.yview)

        self.tree.heading("match_id", text="MATCH ID")
        self.tree.heading("date", text="DATE")
        self.tree.heading("opposition", text="OPPOSITION")
        self.tree.heading("venue", text="VENUE")

        self.tree.column("match_id", width=260, anchor="center")
        self.tree.column("date", width=120, anchor="center")
        self.tree.column("opposition", width=250, anchor="center")
        self.tree.column("venue", width=120, anchor="center")

        self.load_matches()

    def clear_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def load_matches(self):
        self.clear_tree()
        term = self.search_var.get().strip()
        filters = {}
        if term:
            filters["opposition"] = term

        matches = self.match_db.search_match(self.current_user, filters)

        for m in matches:
            match_id = str(m.get("_id", ""))
            self.tree.insert(
                "",
                "end",
                iid=match_id,
                values=(
                    match_id,
                    m.get("match_date", ""),
                    m.get("opposition", ""),
                    Venue.get_value(m.get("venue", ""))
                )
            )

    def delete_match(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("ERROR", "SELECT A MATCH")
            return

        match_id = selected[0]
        values = self.tree.item(match_id, "values")

        confirm_deletion = messagebox.askyesno("CONFIRM DELETION?",
                                               "ARE YOU SURE YOU WANT TO DELETE THIS MATCH")

        if not confirm_deletion:
            return

        deleted = self.match_db.delete_match(self.current_user, match_id)
        if not deleted:
            messagebox.showerror("ERROR", "DELETE FAILED")
            return

        messagebox.showinfo("SUCCESS", "MATCH DELETED")
        self.load_matches()

    def go_back(self):
        self.window.destroy()
        self.parent.deiconify()