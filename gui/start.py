import tkinter as tk
from gui.baseWindow import BaseWindow


class StartWindow(BaseWindow):
    def __init__(self, root):
        #Inherits BaseWindow
        super(). __init__(root)
        self.window = root
        self.window.title("SS - START SCREEN")

        self.center_window(800, 550)
        self.create_widgets()

    def create_widgets(self):
        #Creates main frame to add widgets in
        main_frame = self.create_main_frame()
        self.create_start_header(main_frame, "Select the best possible XI for your next match using real performance data and smart analysis.\n"
                                             "Let's create your winning team!")

        #Content Frame Created to divide page into different parts clearly
        content_frame = tk.Frame(main_frame, borderwidth=3, relief="solid")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        title_label = tk.Label(
            content_frame, text="SMART SKIPPER",
            font=("Arial", 50, "bold"),
        )
        title_label.pack(pady=40)

        # subtitle_label = tk.Label(
        #     content_frame, text=("Select the best possible XI using real performance data.\n"
        #                         "Smart analysis to create your winning team!")
        #
        # )
        # subtitle_label.pack(pady=30)

        #REGISTER & LOGIN BUTTONS
        buttons = tk.Frame(content_frame)
        buttons.pack(pady=30)

        tk.Button(
            buttons, text="REGISTER", width=15, height=3,
            command=self.open_registration

        ).grid(row=0, column=0, padx=30)

        tk.Button(
            buttons, text="LOGIN", width=15, height=3,
            command=self.open_login
        ).grid(row=0, column=1, padx=30)

    #FUNCTIONS TO OPEN REGISTRATION AND LOGIN PAGES
    def open_registration(self):
        from gui.auth import RegistrationWindow
        self.window.withdraw()
        RegistrationWindow(tk.Toplevel(self.window), self.window)

    def open_login(self):
        from gui.auth import LoginWindow
        self.window.withdraw()
        LoginWindow(tk.Toplevel(self.window), self.window)





















