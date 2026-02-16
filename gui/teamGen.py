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

    def get_start_date(self, period: str) -> datetime:
        now = datetime.now(timezone.utc)
        if period == TimePeriod.get_key("LAST MONTH"):
            return now - timedelta(days=30)
        if period == TimePeriod.get_key("LAST 3 MONTHS"):
            return now - timedelta(days=90)
        if period == TimePeriod.get_key("LAST 6 MONTHS"):
            return now - timedelta(days=180)
        if period == TimePeriod.get_key("LAST YEAR"):
            return now - timedelta(days=365)

        raise ValueError ("Invalid time period")


    def save_match_filters(self):

        match_type_value = self.match_type_var.get()
        match_format_value = self.match_format_var.get()
        venue_value = self.venue_var.get()
        time_period_value = self.period_var.get()

        if not match_type_value or not match_format_value or not venue_value or not time_period_value:
            messagebox.showerror("Error", "Please fill in all required fields")
            return


        selected_time_period = TimePeriod.get_key(time_period_value)
        start_date = self.get_start_date(selected_time_period)

        match_filters = {
            "match_type": MatchType.get_key(match_type_value),
            "match_format": MatchFormat.get_key(match_format_value),
            "venue": Venue.get_key(venue_value),
            "start_date": start_date
        }

        self.match_filters = match_filters

        self.window.withdraw()
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
        #tk.Label(form, text= "SELECT TEAM COMPOSITION:", font=("Arial", 12)).grid(row=0, padx=20, pady=10)


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
            batters = int(self.batters_var.get())
            spinners = int(self.spinners_var.get())
            pacers = int(self.pacers_var.get())
            all_rounders = int(self.all_rounders_var.get())
            wk = int(self.wk_var.get())

        except ValueError:
            messagebox.showerror("ERROR", "ALL DROPDOWNS MUST BE SELECTED")
            return

        total = batters + spinners + pacers + all_rounders + wk

        if total != 11:
            messagebox.showerror("ERROR", "TEAM MUST CONSIST ON ONLY 11 PLAYERS")
            return

        balanced_team = (batters== 4 and spinners==2, pacers==2 and all_rounders==2 and wk==1)

        if not balanced_team:
            proceed = messagebox.askyesno("WARNING", "IMBALANCED TEAM SELECTED. DO YOU WISH TO CONTINUE?")
            if not proceed:
                return

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

        #    for player in generated_team:
        #    print(player)

        self.window.withdraw()
        TeamDisplay(tk.Toplevel(self.window), self.window, self.current_user,generated_team)

    def go_back(self):
        self.window.destroy()
        self.parent.deiconify()




"""

class PerformanceMetricsPage(BaseWindow):
    def __init__(self, window, parent, username, match_filters, team_composition):
        super().__init__(window)
        self.window = window
        self.parent= parent
        self.current_user = username
        self.filters = match_filters
        self.team_composition = team_composition
        self.performance_metrics = {}
        self.window.title("SS - TEAM GENERATION")
        self.center_window(850, 650)
        self.create_widgets()


    def create_widgets(self):
        main_frame = self.create_main_frame()
        self.create_header(main_frame, "TEAM GENERATION")
        self.create_sub_header(main_frame, "PERFORMANCE METRICS")

        form = tk.Frame(main_frame)
        form.pack(pady=15)

        self.batter_metric_var = tk.StringVar()
        self.create_dropdown(
            parent=form,
            text="BATTING METRIC",
            variable = self.batter_metric_var,
            values = BatterMetric.list_values(),
            row=0
        )

        self.bowler_metric_var = tk.StringVar()
        self.create_dropdown(
            parent=form,
            text="BOWLING METRIC",
            variable = self.bowler_metric_var,
            values = BowlerMetric.list_values(),
            row=1
        )

        self.wicket_keeper_metric_var = tk.StringVar()
        self.create_dropdown(
            parent=form,
            text="WICKET-KEEPER METRIC",
            variable = self.wicket_keeper_metric_var,
            values = WicketKeeperMetric.list_values() + BatterMetric.list_values(),
            row=2
        )

        self.all_rounders_bat_metric_var = tk.StringVar()
        self.create_dropdown(
            parent=form,
            text="ALL-ROUNDERS (BATTING) METRIC",
            variable = self.all_rounders_bat_metric_var,
            values = BatterMetric.list_values(),
            row =3
        )

        self.all_rounders_bowl_metric_var = tk.StringVar()
        self.create_dropdown(
            parent=form,
            text="ALL-ROUNDERS (BOWLING) METRIC",
            variable = self.all_rounders_bowl_metric_var,
            values = BowlerMetric.list_values(),
            row =4
        )

        self.time_period_var = tk.StringVar()
        self.create_dropdown(
            parent=form,
            text="TIME PERIOD",
            variable=self.time_period_var,
            values=TimePeriod.list_values(),
            row=5
        )

        footer = tk.Frame(main_frame)
        footer.pack(fill="x", side="bottom")

        back_btn = self.create_back_btn(footer, self.go_back)
        back_btn.pack(side="left", padx=20, pady=20)

        save_btn = tk.Button(footer, text="SAVE & GENERATE TEAM", command=self.save_performance_metrics,width=15 )
        save_btn.pack(side="right", padx=20, pady=20)

    def save_performance_metrics(self):

        bat_metric_value = self.batter_metric_var.get()
        bowl_metric_value = self.bowler_metric_var.get()
        wk_metric_value = self.wicket_keeper_metric_var.get()
        ar_bat_value = self.all_rounders_bat_metric_var.get()
        ar_bowl_value = self.all_rounders_bowl_metric_var.get()
        time_period_value = self.time_period_var.get()

        if not (bat_metric_value or bowl_metric_value or wk_metric_value or
                ar_bat_value or ar_bowl_value or time_period_value):
            messagebox.showerror("Error", "Please fill in all required fields")
            return

        performance_metrics = {
            "batter_metric": BatterMetric.get_key(bat_metric_value),
            "bowler_metric": BowlerMetric.get_key(bowl_metric_value),
            "wk_metric": WicketKeeperMetric.get_key(wk_metric_value),
            "all_rounder_batting_metric": BatterMetric.get_key(ar_bat_value),
            "all_rounder_bowling_metric": BowlerMetric.get_key(ar_bowl_value),
            "time_period": TimePeriod.get_key(time_period_value)
        }

        self.performance_metrics = performance_metrics


    def go_back(self):
        self.window.destroy()
        self.parent.deiconify()

"""