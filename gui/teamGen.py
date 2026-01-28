import tkinter as tk
from gui.baseWindow import BaseWindow
from bff.enums import (MatchType, MatchFormat, Venue,
                       BatterMetric, BowlerMetric, WicketKeeperMetric, TimePeriod)

class FixtureDetailsPage(BaseWindow):
    def __init__(self, window, parent, username):
        super().__init__(window)
        self.window = window
        self.parent = parent
        self.current_user = username
        self.window.title("SS - TEAM GENERATION")
        self.center_window(800, 600)
        self.create_widgets()


    def create_widgets(self):
        main_frame = self.create_main_frame()
        self.create_header(main_frame, "TEAM GENERATION")
        self.create_sub_header(main_frame, "UPCOMING FIXTURE DETAILS")

        form = tk.Frame(main_frame)
        form.pack(pady=70)

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

        footer = tk.Frame(main_frame)
        footer.pack(fill=tk.X, side=tk.BOTTOM)

        back_btn = self.create_back_btn(footer, self.go_back)
        back_btn.pack(side=tk.LEFT, padx=20, pady=20)

        save_btn = tk.Button(footer, text="SAVE", command= self.open_team_composition_page,width=15 )
        save_btn.pack(side=tk.RIGHT, padx=20, pady=20)

    def open_team_composition_page(self):
        self.window.withdraw()
        TeamCompositionPage(tk.Toplevel(self.window), self.window, self.current_user)

    def go_back(self):
        self.window.destroy()
        self.parent.deiconify()

class TeamCompositionPage(BaseWindow):
    def __init__(self, window, parent, username):
        super().__init__(window)
        self.window = window
        self.parent = parent
        self.current_user = username

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


        #tk.Label(form, text="SELECT TEAM COMPOSITION: ", font=("Arial", 12)).grid(row=0, padx=20, pady=10)
        self.create_dropdown(form, text="BATTERS", variable='', values=[0,1,2,3,4,5,6,7,8,9,10,11], row=1)
        self.create_dropdown(form, text="SPINNERS", variable='', values=[0,1,2,3,4,5,7,8,9,10,11], row=2)
        self.create_dropdown(form, text="PACERS", variable='', values=[0,1,2,3,4,5,6,7,8,9,10,11], row=3)
        self.create_dropdown(form, text="ALL-ROUNDERS", variable='', values=[0,1,2,3,4,5,6,7,8,9,10,11], row=4)
        self.create_dropdown(form, text="WICKET-KEEPERS", variable='', values=[0,1,2,3,4,5,6,7,8,9,10,11], row=5)

        self.match_type_var = tk.StringVar()
        self.create_dropdown(
            parent=form,
            text="MATCH TYPE: ",
            variable=self.match_type_var,
            values=MatchType.list_values(),
            row=6
        )

        self.match_format_var = tk.StringVar()
        self.create_dropdown(
            parent=form,
            text="MATCH FORMAT: ",
            variable=self.match_format_var,
            values=MatchFormat.list_values(),
            row=7
        )

        self.venue_var = tk.StringVar()
        self.create_dropdown(
            parent=form,
            text="VENUE: ",
            variable=self.venue_var,
            values=Venue.list_values(),
            row=8
        )


        footer = tk.Frame(main_frame)
        footer.pack(fill=tk.X, side=tk.BOTTOM)

        back_btn = self.create_back_btn(footer, self.go_back)
        back_btn.pack(side=tk.LEFT, padx=20, pady=20)

        save_btn = tk.Button(footer, text="SAVE", command= self.open_performance_metrics_page, width=15 )
        save_btn.pack(side=tk.RIGHT, padx=20, pady=20)

    def open_performance_metrics_page(self):
        self.window.withdraw()
        PerformanceMetricsPage(tk.Toplevel(self.window), self.window, self.current_user)

    def go_back(self):
        self.window.destroy()
        self.parent.deiconify()



class PerformanceMetricsPage(BaseWindow):
    def __init__(self, window, parent, username):
        super().__init__(window)
        self.window = window
        self.parent= parent
        self.current_user = username
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

        self.all_rounders_metric_var = tk.StringVar()
        self.create_dropdown(
            parent=form,
            text="ALL-ROUNDERS (BATTING) METRIC",
            variable = self.all_rounders_metric_var,
            values = BatterMetric.list_values(),
            row =3
        )

        self.all_rounders_metric_var = tk.StringVar()
        self.create_dropdown(
            parent=form,
            text="ALL-ROUNDERS (BOWLING) METRIC",
            variable = self.all_rounders_metric_var,
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
        footer.pack(fill=tk.X, side=tk.BOTTOM)

        back_btn = self.create_back_btn(footer, self.go_back)
        back_btn.pack(side=tk.LEFT, padx=20, pady=20)

        save_btn = tk.Button(footer, text="SAVE", command= '',width=15 )
        save_btn.pack(side=tk.RIGHT, padx=20, pady=20)

    def go_back(self):
        self.window.destroy()
        self.parent.deiconify()







