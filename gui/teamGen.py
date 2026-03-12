import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timezone, timedelta
from gui.baseWindow import BaseWindow
from bff.database import TeamGeneratorDB
from bff.enums import (MatchType, MatchFormat, Venue, TimePeriod)
from gui.teamDisplay import TeamDisplay


class FixtureDetailsPage(BaseWindow):
    def __init__(self, window, parent, username):
        super().__init__(window)
        self.window = window
        self.parent = parent
        self.current_user = username
        self.match_filters = {}
        self.window.title("SS - TEAM GENERATION")
        self.center_window(800, 600)
        self.create_widgets()


    def create_widgets(self):
        main_frame = self.create_main_frame()
        self.create_header(main_frame, "TEAM GENERATION")
        self.create_sub_header(main_frame, "UPCOMING FIXTURE DETAILS")

        form = tk.Frame(main_frame)
        form.pack(pady=40)

        self.match_filters.clear()

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

        self.period_var = tk.StringVar()
        self.create_dropdown(
            parent=form,
            text="PERIOD: ",
            variable=self.period_var,
            values=TimePeriod.list_values(),
            row=3
        )


        footer = tk.Frame(main_frame)
        footer.pack(fill="x", side="bottom")

        back_btn = self.create_back_btn(footer, self.go_back)
        back_btn.pack(side=tk.LEFT, padx=20, pady=20)

        save_btn = tk.Button(footer, text="SAVE", command= self.save_match_filters,width=15 )
        save_btn.pack(side="right", padx=20, pady=20)

    def get_start_date(self, period_key: str) -> datetime:
        # Get the current date and time in UTC
        now = datetime(2026, 2, 21, 14, 23, 21, 231345)
        if period_key == "LM":
            return now - timedelta(days=30) #subtract 30 days from today
        if period_key == "L3M":
            return now - timedelta(days=90) #subtract 90 days from today
        if period_key == "L6M":
            return now - timedelta(days=180) #subtract 180 days from today
        if period_key == "L12M":
            return now - timedelta(days=365) #subtract 365 days from today

        raise ValueError ("Invalid time period")


    def save_match_filters(self):
        #Get the selected values from the dropdown menus
        match_type_value = self.match_type_var.get()
        match_format_value = self.match_format_var.get()
        venue_value = self.venue_var.get()
        time_period_value = self.period_var.get()

        #Check if any required field is empty
        if not match_type_value or not match_format_value or not venue_value or not time_period_value:
            messagebox.showerror("Error", "Please fill in all required fields")
            return
        confirm_match_filters = messagebox.askyesno("CONFIRM CHOICE", "DO YOU WISH TO PROCEED WITH THESE MATCH FILTERS?")
        if not confirm_match_filters:
            return

        #Convert the selected time period display value to enum key
        selected_time_period = TimePeriod.get_key(time_period_value)
        #Convert the time period into a real start date
        start_date = self.get_start_date(selected_time_period)
        print(f"START DATE: {start_date}") #TESTING

        #Dictionary to store all selected filters
        match_filters = {
            "match_type": MatchType.get_key(match_type_value),
            "match_format": MatchFormat.get_key(match_format_value),
            "venue": Venue.get_key(venue_value),
            "start_date": start_date
        }
        #Save filters to the class so they can be accessed later
        self.match_filters = match_filters
        print(f"MATCH FILTERS: {match_filters}") #TESTING
        self.window.withdraw()
        #Pass selected filters to next page
        TeamCompositionPage(tk.Toplevel(self.window), self.window, self.current_user, self.match_filters)

    def go_back(self):
        self.window.destroy()
        self.parent.deiconify()

class TeamCompositionPage(BaseWindow):
    def __init__(self, window, parent, username, match_filters):
        super().__init__(window)
        self.window = window
        self.parent = parent
        self.team_generator_db = TeamGeneratorDB()
        self.current_user = username
        self.match_filters = match_filters
        self.match_type_filter = match_filters["match_type"]
        self.match_format_filter = match_filters["match_format"]
        self.match_venue_filter = match_filters["venue"]
        self.start_date = match_filters["start_date"]
        self.window.title("SS - TEAM GENERATION")
        self.center_window(900, 700)

        self.create_widgets()


    def create_widgets(self):
        main_frame = self.create_main_frame()
        self.create_header(main_frame, "TEAM GENERATION")
        self.create_sub_header(main_frame," RECOMMENDED TEAM COMPOSITION:"
                                           "\n\n4 BATTERS, 3 BOWLERS, 3 ALL_ROUNDERS, 1 WICKET-KEEPER",)

        form = tk.Frame(main_frame)
        form.pack(pady=0)

        self.batters_var = tk.IntVar()
        self.create_dropdown(form, text="BATTERS", variable=self.batters_var, values=list(range(12)), row=1)
        self.spinners_var = tk.IntVar()
        self.create_dropdown(form, text="SPINNERS", variable=self.spinners_var, values=list(range(12)), row=2)
        self.pacers_var = tk.IntVar()
        self.create_dropdown(form, text="PACERS", variable=self.pacers_var, values=list(range(12)), row=3)
        self.all_rounders_var = tk.IntVar()
        self.create_dropdown(form, text="ALL-ROUNDERS", variable=self.all_rounders_var, values=list(range(12)), row=4)
        self.wk_var = tk.IntVar()
        self.create_dropdown(form, text="WICKET-KEEPERS", variable=self.wk_var, values=list(range(12)), row=5)

        footer = tk.Frame(main_frame)
        footer.pack(fill="x", side="bottom")

        back_btn = self.create_back_btn(footer, self.go_back)
        back_btn.pack(side=tk.LEFT, padx=20, pady=20)

        save_btn = tk.Button(footer, text="SAVE & GENERATE TEAM", command= self.save_team_composition, width=20)
        save_btn.pack(side="right", padx=20, pady=20)

    def save_team_composition(self):
        try:
            #Convert dropdown values to integers
            batters = int(self.batters_var.get())
            spinners = int(self.spinners_var.get())
            pacers = int(self.pacers_var.get())
            all_rounders = int(self.all_rounders_var.get())
            wk = int(self.wk_var.get())
        except ValueError:
            #If any dropdown is not selected properly, show error
            messagebox.showerror("ERROR", "ALL DROPDOWNS MUST BE SELECTED")
            return

        #Calculate total number of selected players
        total = batters + spinners + pacers + all_rounders + wk

        if total != 11: #Ensure team has exactly 11 players
            messagebox.showerror("ERROR", "TEAM MUST CONSIST ON ONLY 11 PLAYERS")
            return

        #Check if team matches predefined balanced structure
        balanced_team = (batters== 4 and spinners==2 and pacers==2 and all_rounders==2 and wk==1)

        if not balanced_team:
            proceed = messagebox.askyesno("WARNING", "IMBALANCED TEAM SELECTED. DO YOU WISH TO CONTINUE?")
            if not proceed:
                return

        confirm_team = messagebox.askyesno("CONFIRM", "CONFIRM TEAM COMPOSITION?")
        if not confirm_team:
            return

        #Call database method to generate team using selected filters and limits
        generated_team = self.team_generator_db.generate_team(username=self.current_user,
                                    match_type=self.match_type_filter,
                                    match_format=self.match_format_filter,
                                    venue=self.match_venue_filter,
                                    from_date=self.start_date,
                                    batter_limit=batters,
                                    pacer_limit=pacers,
                                    spinner_limit=spinners,
                                    all_rounder_limit=all_rounders,
                                    wk_limit=wk)
        #TESTING
        for player in generated_team:
            print(player)

        self.window.withdraw()
        TeamDisplay(tk.Toplevel(self.window), self.window, self.current_user,generated_team)

    def go_back(self):
        self.window.destroy()
        self.parent.deiconify()
