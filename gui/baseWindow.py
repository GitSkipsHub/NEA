import tkinter as tk
from tkinter import ttk

class BaseWindow:
    def __init__(self, window):
        self.window = window

    #Centres Window on Device Screen
    def center_window(self, width, height):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - width)//2
        y = (screen_height - height)//2
        self.window.geometry(f"{width}x{height}+{x}+{y}")

    #Creates Main Container to add widgets
    def create_main_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(fill=tk.BOTH, expand=True) #Stretches header border horizontally through the window
        return frame

    #Creates Header on start Page
    def create_start_header(self, parent, text):
        start_header_frame = tk.Frame(
            parent,
            height=80,
            highlightbackground="dodger blue",
            highlightthickness=5,
        )
        start_header_frame.pack(fill=tk.X)
        start_header_frame.pack_propagate(False) #Prevents header from shrinking or increasing depending on text size

        label = tk.Label(
            start_header_frame,
            text=text,
            font=("Arial", 12, "bold")
        )
        label.pack(pady=15)
        return start_header_frame

    #Creates Header that can be used on multiple pages
    def create_header(self, parent, text):
        header_frame = tk.Frame(
            parent,
            height=80,
            highlightbackground="dim gray",
            highlightthickness=6,
        )
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(True)

        label = tk.Label(
            header_frame,
            text=text,
            font=("Arial", 45, "bold")
        )
        label.pack(pady=10)
        return header_frame

    #Creates subheading that can be used on multiple pages
    def create_sub_header(self, parent, text):
        sub_header_frame = tk.Frame(
            parent,
            height=50,
            highlightbackground="white",
            highlightthickness=2,
        )

        sub_header_frame.pack(fill=tk.X, pady=20, padx=20,)
        sub_header_frame.pack_propagate(True)

        label = tk.Label(
            sub_header_frame,
            text=text,
            font=("Arial", 20,)
        )
        label.pack(pady=20)
        return sub_header_frame

    def create_dropdown(self, parent, text, variable, values, row):
        label = tk.Label(
            parent,
            text=text,
        )
        label.grid(column=0, row=row, pady=10, sticky="e")

        combo = ttk.Combobox(
            parent,
            textvariable=variable,
            values=values,
            state="readonly",
            width=20,
        )
        combo.grid(column=1, row=row, pady=10)

        return combo

    #Creates Back Button that can be used for multiple pages
    def create_back_btn(self, parent, back_command): #parent tells us where the button goes --> which window / which container
        back_btn = tk.Button(
            parent,
            text="BACK",
            width=15,
            command=back_command, # PlaceHolder for command function that will be taken in

        )
        return back_btn






