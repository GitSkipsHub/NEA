import tkinter as tk
from gui.baseWindow import BaseWindow
from bff.enums import MatchType, MatchFormat, Venue, Result, TossResult

class MatchManagementPage(BaseWindow):
    def __init__(self, window, parent):
        super().__init__(window)
        self.window = window
        self.parent = parent

        self.window.title("SS - MATCH MANAGEMENT")
        self.center_window(800, 600)

        self.create_widgets()

    def create_widgets(self):
        main_frame = self.create_main_frame()
        self.create_header(main_frame, "MATCH MANAGEMENT")

        footer = tk.Frame(main_frame)
        footer.pack(fill=tk.X, side=tk.BOTTOM)

        back_btn = self.create_back_btn(footer, self.go_back)
        back_btn.pack(side=tk.LEFT, padx=20, pady=20)

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
        CreateMatchDetailsPage(tk.Toplevel(self.window), self.window)


    def go_back(self):
        self.window.destroy()
        self.parent.deiconify()


class CreateMatchDetailsPage(BaseWindow):
    def __init__(self, window, parent):
        super().__init__(window)
        self.window = window
        self.parent = parent

        self.window.title("SS - MATCH DETAILS")
        self.center_window(850,650)

        self.create_widgets()

    def create_widgets(self):
        main_frame = self.create_main_frame()
        self.create_header(main_frame, "CREATE MATCH")
        self.create_sub_header(main_frame, "MATCH DETAILS")

        form = tk.Frame(main_frame)
        form.pack(pady=20)

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
        self.ground_name_input.grid(column=1, row=4, pady=10)

        tk.Label(form, text="OPPOSITION: ").grid(column=0, row=5, pady=10, sticky="e")
        self.opposition_input = tk.Entry(form)
        self.opposition_input.grid(column=1, row=5, pady=10)

        tk.Label(form, text="DATE (YYYY-MM-DD): ").grid(column=0, row=6, pady=10, sticky="e")
        self.date_input = tk.Entry(form)
        self.date_input.grid(column=1, row=6, pady=10)



        footer = tk.Frame(main_frame)
        footer.pack(fill=tk.X, side=tk.BOTTOM)

        back_btn = self.create_back_btn(footer, self.go_back)
        back_btn.pack(side=tk.LEFT, padx=20, pady=20)

    def go_back(self):
        self.window.destroy()
        self.parent.deiconify()


