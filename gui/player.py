import tkinter as tk
from tkinter import ttk, messagebox
from gui.baseWindow import BaseWindow
from bff.database import PlayerDB
from bff.enums import PlayerRole, BattingStyle, BowlingStyle
from datetime import datetime
from bff.models import Player


class PlayerManagementWindow(BaseWindow):
    def __init__(self, window, parent, username):
        super().__init__(window)
        self.current_user = username
        self.window = window
        self.parent = parent

        self.window.title("SS - PLAYER MANAGEMENT")
        self.center_window(800, 600)
        self.create_widgets()

    def create_widgets(self):
        main_frame = self.create_main_frame()
        self.create_header(main_frame, "PLAYER MANAGEMENT")

        footer = tk.Frame(main_frame)
        footer.pack(fill="x", side="bottom")

        back_btn = self.create_back_btn(footer, self.go_back)
        back_btn.pack(side=tk.LEFT, padx=20, pady=20)

        tk.Button(main_frame,
                  text="CREATE PLAYER",
                  width=15,
                  height=3,
                  command=self.open_create_player_page,
                  ).pack(pady=30)

        tk.Button(main_frame,
                  text="UPDATE PLAYER",
                  width=15,
                  height=3,
                  command=self.open_update_player_window
                  ).pack(pady=20)
        tk.Button(main_frame,
                  text="DELETE PLAYER",
                  width=15,
                  height=3,
                  command=self.open_delete_player_window
                  ).pack(pady=30)

    def open_create_player_page(self):
        self.window.withdraw()
        CreatePlayerWindow(tk.Toplevel(self.window), self.window, self.current_user)

    def open_update_player_window(self):
        self.window.withdraw()
        UpdatePlayerWindow(tk.Toplevel(self.window), self.window, self.current_user)

    def open_delete_player_window(self):
        self.window.withdraw()
        DeletePlayerWindow(tk.Toplevel(self.window), self.window, self.current_user)

    def go_back(self):
        self.window.destroy()
        self.parent.deiconify()


class CreatePlayerWindow(BaseWindow):
    def __init__(self, window, parent, username):
        super().__init__(window)
        self.window = window
        self.parent = parent
        self.window.title("SS - CREATE PLAYER")
        self.center_window(800, 600)
        self.current_user = username
        self.player_db = PlayerDB()
        self.create_widgets()

    def create_widgets(self):

        main_frame = self.create_main_frame()
        self.create_header(main_frame, "PLAYER CREATION")

        form = tk.Frame(main_frame)
        form.pack(pady=50)

        footer = tk.Frame(main_frame)
        footer.pack(fill="x", side="bottom")

        tk.Label(form, text="FIRST NAME : ").grid(column=0, row=0, pady=10, sticky="e")
        self.first_name_input = tk.Entry(form)
        self.first_name_input.configure(highlightthickness=3, highlightbackground="dodger blue")
        self.first_name_input.grid(column=1, row=0, pady=10)

        tk.Label(form, text="LAST NAME : ").grid(column=0, row=1, pady=10, sticky="e")
        self.last_name_input = tk.Entry(form)
        self.last_name_input.configure(highlightthickness=3, highlightbackground="dodger blue")
        self.last_name_input.grid(column=1, row=1, pady=10)

        tk.Label(form, text="DATE OF BIRTH (YYYY-MM-DD): ").grid(column=0, row=2, pady=10, sticky="e")
        self.dob_input = tk.Entry(form)
        self.dob_input.configure(highlightthickness=3, highlightbackground="dodger blue")
        self.dob_input.grid(column=1, row=2, pady=10)

        # tk.Label(form, text="PLAYER ROLE: ").grid(column=0, row=3, pady=10, sticky="e")
        # self.player_role_var = tk.StringVar()
        # player_role_values = PlayerRole.list_values()
        # ttk.Combobox(form,
        #              textvariable=self.player_role_var,
        #              values=player_role_values,
        #              state="readonly",
        #              width=20,
        #              ).grid(column=1, row=3, pady=10)
        #
        # tk.Label(form, text="BATTING STYLE: ").grid(column=0, row=4, pady=10, sticky="e")
        # self.batting_style_var = tk.StringVar()
        # batting_style_values = BattingStyle.list_values()
        # ttk.Combobox(form,
        #              textvariable=self.batting_style_var,
        #              values=batting_style_values,
        #              state="readonly",
        #              width=20,
        #              ).grid(column=1, row=4, pady=10)
        #
        # tk.Label(form, text="BOWLING STYLE: ").grid(column=0, row=5, pady=10, sticky="e")
        # self.bowling_style_var = tk.StringVar()
        # bowling_style_values = BowlingStyle.list_values()
        # ttk.Combobox(form,
        #              textvariable=self.bowling_style_var,
        #              values=bowling_style_values,
        #              state="readonly",
        #              width=20,
        #              ).grid(column=1, row=5, pady=10)


        self.player_role_var = tk.StringVar()
        self.create_dropdown(
            parent=form,
            text="PLAYER ROLE: ",
            variable=self.player_role_var,
            values=PlayerRole.list_values(),
            row=3,
        )

        self.batting_style_var = tk.StringVar()
        self.create_dropdown(
            parent=form,
            text="BATTING STYLE: ",
            variable=self.batting_style_var,
            values=BattingStyle.list_values(),
            row=4,
        )

        self.bowling_style_var = tk.StringVar()
        self.create_dropdown(
            parent=form,
            text="BOWLING STYLE: ",
            variable=self.bowling_style_var,
            values=BowlingStyle.list_values(),
            row=5,
        )


        back_btn = self.create_back_btn(footer, self.go_back)
        back_btn.pack(side=tk.LEFT, padx=20, pady=20)

        #tk.Button(footer, text="SAVE", width=15,).pack(side=tk.RIGHT, padx=20, pady=20)

        save_btn = tk.Button(footer, text="SAVE", command= self.save_player, width=15 )
        save_btn.pack(side="right", padx=20, pady=20)

    def save_player(self):
        #Gets all inputs from entries
        first_name = self.first_name_input.get().strip()
        last_name = self.last_name_input.get().strip()
        dob = self.dob_input.get().strip()
        player_role_value = self.player_role_var.get().strip()
        batting_style_value = self.batting_style_var.get().strip()
        bowling_style_value = self.bowling_style_var.get().strip()

        if not first_name or not last_name or not dob or not player_role_value or not bowling_style_value or not batting_style_value:
            messagebox.showerror("Error", "Please fill in all required fields")
            return

        #Checks if datetime is in correct format
        try:
            datetime.strptime(dob, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("ERROR", "DOB must be in YYYY-MM-DD format (e.g., 2007-04-19)")
            return

        #Maps fields into Player Object
        player_obj = Player(
            player_id="",  # Temporary (Mongo creates _id)
            username=self.current_user,
            first_name=first_name,
            last_name= last_name,
            date_of_birth=dob,
            player_role=PlayerRole.get_key(player_role_value),
            batting_style=BattingStyle.get_key(batting_style_value),
            bowling_style=BowlingStyle.get_key(bowling_style_value)
        )

        #Converts Player Object to dict and saves player
        if self.player_db.create_player(self.current_user, player_obj.to_dict()):
            messagebox.showinfo("SUCCESS", "Player Created")
            self.go_back()
            return
        else:
            messagebox.showerror("ERROR", "Failed to Create Player")
            return

    def go_back(self):
        self.window.destroy()
        self.parent.deiconify()


class UpdatePlayerWindow(BaseWindow):
    def __init__(self, window, parent, username):
        super().__init__(window)
        self.selected_player_id = None
        self.window = window
        self.parent = parent
        self.current_user = username
        self.player_db = PlayerDB()
        self.window.title("SS - PLAYER MANAGEMENT")
        self.center_window(1250, 900)
        self.create_widgets()

    def create_widgets(self):
        main_frame = self.create_main_frame()
        self.create_header(main_frame, "UPDATE PLAYER")

        search_frame = tk.Frame(main_frame)
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="SEARCH NAME: ", font=("Arial", 15, "bold")).grid(
            row=0, column=1, padx=30, pady=20
        )
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.configure(highlightthickness=3, highlightbackground="dodger blue")
        search_entry.grid(row=0, column=2, padx=10, pady=10)

        table_frame = tk.Frame(main_frame)
        table_frame.pack(fill="both", expand=True, padx=30, pady=5)

        #Defined columns that will appear in the table
        player_columns = (
            "player_id", "created_date", "first_name", "last_name",
            "date_of_birth", "player_role", "batting_style", "bowling_style"
        )
        #Vertical scrollbar
        y_scrollbar = ttk.Scrollbar(table_frame, orient="vertical")
        y_scrollbar.pack(side="right", fill="y")

        #Horizontal scrollbar
        x_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal")
        x_scrollbar.pack(side="bottom", fill="x")

        #Treeview table widget
        self.tree = ttk.Treeview(
            table_frame,
            columns=player_columns,
            show="headings",
            height=10,
            yscrollcommand=y_scrollbar.set,
            xscrollcommand=x_scrollbar.set
        )
        self.tree.pack(side="left", fill="both", expand=True)

        #Linking scrollbars to Treeview
        x_scrollbar.config(command=self.tree.xview)
        y_scrollbar.config(command=self.tree.yview)

        #Set column headings
        self.tree.heading("player_id", text="ID")
        self.tree.heading("created_date", text="Created Date")
        self.tree.heading("first_name", text="First Name")
        self.tree.heading("last_name", text="Last Name")
        self.tree.heading("date_of_birth", text="DOB")
        self.tree.heading("player_role", text="Player Role")
        self.tree.heading("batting_style", text="Batting Style")
        self.tree.heading("bowling_style", text="Bowling Style")

        #Set column widths
        self.tree.column("player_id", width=200)
        self.tree.column("created_date", width=160)
        self.tree.column("first_name", width=120)
        self.tree.column("last_name", width=120)
        self.tree.column("date_of_birth", width=120)
        self.tree.column("player_role", width=120)
        self.tree.column("batting_style", width=120)
        self.tree.column("bowling_style", width=150)

        #Bind selection event
        self.tree.bind("<<TreeviewSelect>>", self.select_on_player) #When a row is clicked, select_on_player() is triggered

        footer = tk.Frame(main_frame)
        footer.pack(fill="x", side="bottom")

        back_btn = self.create_back_btn(footer, self.go_back)
        back_btn.pack(side=tk.LEFT, padx=10, pady=10)

        update_button = tk.Button(footer, text="UPDATE PLAYER", command=self.update_player, width=15)
        update_button.pack(side="right", pady=10, padx=10)

        search_button = tk.Button(footer, text="SEARCH", command=self.search_player, width=15)
        search_button.pack(side="top", padx=10, pady=10)

        form = tk.Frame(main_frame)
        form.pack(pady=20)

        tk.Label(form, text="FIRST NAME: ").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        tk.Label(form, text="LAST NAME: ").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        tk.Label(form, text="DATE OF BIRTH (YYYY-MM-DD): ").grid(row=2, column=0, padx=10, pady=10, sticky="e")

        self.first_name_edit = tk.StringVar()
        self.last_name_edit = tk.StringVar()
        self.dob_edit = tk.StringVar()
        self.player_role_edit = tk.StringVar()
        self.batting_style_edit = tk.StringVar()
        self.bowling_style_edit = tk.StringVar()

        fname_entry = tk.Entry(form, textvariable=self.first_name_edit, width=25)
        fname_entry.grid(row=0, column=1, padx=10)
        fname_entry.configure(highlightthickness=3, highlightbackground="dodger blue")

        lname_entry = tk.Entry(form, textvariable=self.last_name_edit, width=25)
        lname_entry.grid(row=1, column=1, padx=10)
        lname_entry.configure(highlightthickness=3, highlightbackground="dodger blue")

        dob_entry = tk.Entry(form, textvariable=self.dob_edit, width=25)
        dob_entry.grid(row=2, column=1, padx=10)
        dob_entry.configure(highlightthickness=3, highlightbackground="dodger blue")

        self.create_dropdown(
            parent=form,
            text="PLAYER ROLE: ",
            variable=self.player_role_edit,
            values=PlayerRole.list_values(),
            row=3
        )
        self.create_dropdown(
            parent=form,
            text="BATTING STYLE: ",
            variable=self.batting_style_edit,
            values=BattingStyle.list_values(),
            row=4
        )
        self.create_dropdown(
            parent=form,
            text="BOWLING STYLE: ",
            variable=self.bowling_style_edit,
            values=BowlingStyle.list_values(),
            row=5
        )

        self.search_player()

    #Remove all existing rows from the Treeview table --> ensures old results are cleared before new search results are inserted
    def clear_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def search_player(self):
        #Clear table so results don't stack on top of each other
        self.clear_tree()
        print("SEARCH TREE FUNCTION CALLED & RUNNING")
        #Search player with via search term
        term = self.search_var.get()
        players = self.player_db.search_player(self.current_user, term)

        for player in players:
            #Extract the created_date field
            formatted_date = player.get("created_date")
            #If the date is a datetime object, convert it into readable string format
            if isinstance(formatted_date, datetime):
                formatted_date = formatted_date.strftime("%Y-%m-%d %H:%M:%S")

            #Convert MongoDB dictionary into Player Object
            player_obj = Player.from_dict(player)
            #Insert the player data into the Treeview table
            self.tree.insert(
                "",         #Insert at root level (not nested)
                "end",       #Add to bottom of table
                values=(
                    player_obj.player_id,
                    formatted_date,
                    player_obj.first_name,
                    player_obj.last_name,
                    player_obj.date_of_birth,
                    PlayerRole.get_value(player_obj.player_role),
                    BattingStyle.get_value(player_obj.batting_style),
                    BowlingStyle.get_value(player_obj.bowling_style),
                )
            )

    #Function  runs when a user selects a row in the table
    def select_on_player(self, event):
        #Get currently selected row
        selected = self.tree.selection()
        #If no row is selected --> exit function
        if not selected:
            # ERROR #1: does NOT reset selected_player_id when nothing selected
            return

        #Extract all values stored in the selected row
        values = self.tree.item(selected[0], "values")

        #Store the selected player's ID (used later for updating)
        self.selected_player_id = values[0]

        #Populate input fields with selected player's data
        self.first_name_edit.set(values[2])
        self.last_name_edit.set(values[3])
        self.dob_edit.set(values[4])
        #Display values (e.g. "RIGHT HAND"), not Enum keys
        self.player_role_edit.set(values[5])
        self.batting_style_edit.set(values[6])
        self.bowling_style_edit.set(values[7])

    def update_player(self):
        #Check if a player has been selected from the table
        if not self.selected_player_id:
            messagebox.showerror("ERROR", "SELECT PLAYER FROM THE TABLE FIRST")
            return

        #Get updated values from the input fields and remove extra spaces
        fname = self.first_name_edit.get().strip()
        lname = self.last_name_edit.get().strip()
        dob = self.dob_edit.get().strip()
        p_role_value = self.player_role_edit.get().strip()
        bat_style_value = self.batting_style_edit.get().strip()
        bowl_style_value = self.bowling_style_edit.get().strip()

        if not fname or not lname or not dob or not p_role_value or not bat_style_value or not bowl_style_value:
            messagebox.showerror("ERROR", "FILL IN ALL REQUIRED FIELDS")
            return

        #Validate the date format
        try:
            datetime.strptime(dob, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("ERROR", "DOB must be in YYYY-MM-DD format (e.g., 2007-04-19)")
            return

        #Convert dropdown display values back into enum keys for database storage
        update_data = {
            "first_name": fname,
            "last_name": lname,
            "date_of_birth": dob,
            "player_role": PlayerRole.get_key(p_role_value),
            "batting_style": BattingStyle.get_key(bat_style_value),
            "bowling_style": BowlingStyle.get_key(bowl_style_value),
        }

        #Call the database function to update the record
        updated_record = self.player_db.update_player(self.current_user, self.selected_player_id, update_data)
        if updated_record:
            messagebox.showinfo("SUCCESS", "PLAYER UPDATED SUCCESSFULLY")

            #Refreshes Treeview Table
            self.search_player()

            #Reset selected ID after update
            self.selected_player_id = None
        else:
            messagebox.showerror("ERROR", "PLAYER UPDATE FAILED")

    def go_back(self):
        self.window.destroy()
        self.parent.deiconify()



class DeletePlayerWindow(BaseWindow):
    def __init__(self, window, parent, username):
        super().__init__(window)
        self.selected_player_id = None
        self.window = window
        self.parent = parent
        self.current_user = username
        self.player_db = PlayerDB()
        self.window.title("SS - PLAYER MANAGEMENT")
        self.center_window(1200, 700)
        self.create_widgets()


    def create_widgets(self):

        main_frame = self.create_main_frame()
        self.create_header(main_frame, "DELETE PLAYER")

        search_frame = tk.Frame(main_frame)
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="SEARCH NAME: ").grid(row=0, column=0, padx=10, pady=30, sticky="e")
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.configure(highlightthickness=3, highlightbackground="dodger blue")
        search_entry.grid(row=0, column=1, padx=10, pady=10)

        table_frame = tk.Frame(main_frame)
        table_frame.pack(fill="both", expand=True, padx=30, pady=10)

        player_columns = ("player_id", "created_date", "first_name", "last_name", "date_of_birth", "player_role",
                          "batting_style", "bowling_style")

        y_scrollbar = ttk.Scrollbar(table_frame, orient="vertical")
        y_scrollbar.pack(side="right", fill="y")

        x_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal")
        x_scrollbar.pack(side="bottom", fill="x")

        self.tree = ttk.Treeview(table_frame, columns=player_columns, show="headings",
                                 height=10, yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)

        x_scrollbar.config(command=self.tree.xview)
        y_scrollbar.config(command=self.tree.yview)

        self.tree.heading("player_id", text="ID")
        self.tree.heading("created_date", text="Created Date")
        self.tree.heading("first_name", text="First Name")
        self.tree.heading("last_name", text="Last Name")
        self.tree.heading("date_of_birth", text="DOB")
        self.tree.heading("player_role", text="Player Role")
        self.tree.heading("batting_style", text="Batting Style")
        self.tree.heading("bowling_style", text="Bowling Style")

        self.tree.column("player_id", width=200)
        self.tree.column("created_date", width=160)
        self.tree.column("first_name", width=120)
        self.tree.column("last_name", width=120)
        self.tree.column("date_of_birth", width=120)
        self.tree.column("player_role", width=120)
        self.tree.column("batting_style", width=120)
        self.tree.column("bowling_style", width=150)

        self.tree.bind("<<TreeviewSelect>>", self.select_on_player)


        footer = tk.Frame(main_frame)
        footer.pack(fill="x", side="bottom")

        back_btn = self.create_back_btn(footer, self.go_back)
        back_btn.pack(side=tk.LEFT, padx=10, pady=10)

        delete_button = tk.Button(footer, text="DELETE PLAYER", command=self.delete_player, width=15)
        delete_button.pack(side="right", pady=10, padx=10)

        search_button = tk.Button(footer, text="SEARCH", command=self.search_player, width=15)
        search_button.pack(side="top", padx=10, pady=10)

        self.search_player()

    def clear_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def search_player(self):
        self.clear_tree() #Removes all existing rows on tree
        term = self.search_var.get() #reads text entered in search box
        players = self.player_db.search_player(self.current_user, term) #Calls database function passing parameters

        for player in players:
            formatted_date = player.get("created_date")
            if isinstance(formatted_date, datetime):
                formatted_date = formatted_date.strftime("%Y-%m-%d %H:%M:%S") #Formats date in human-readable format

            player_obj = Player.from_dict(player)
            self.tree.insert(
                "", #"" = insert at root level, not nested
                "end", # adds row to bottom of the table
                values=(
                    player_obj.player_id, #index 0
                    formatted_date,             #index 1
                    player_obj.first_name, #index 2
                    player_obj.last_name,
                    player_obj.date_of_birth,
                    PlayerRole.get_value(player_obj.player_role),
                    BattingStyle.get_value(player_obj.batting_style),
                    BowlingStyle.get_value(player_obj.bowling_style), #index 7
                )
            )

    def select_on_player(self, event): #retreives selected row from treeview & returns tuple of item IDs
        selected = self.tree.selection()
        if not selected: #if no row is selected (user clicked empty space) --> exit function
            self.selected_player_id = None
            return

        #From the selected row, extract the data values that were inserted into it
        values = self.tree.item(selected[0], "values") #extracts values stored in that row in the same order they were inserted into the treeview
        self.selected_player_id = values[0] #stores player's unique id so correct record is updated later --> required for MongoDB


    def delete_player(self):
        if not self.selected_player_id:
            messagebox.showerror("ERROR", "SELECT PLAYER FIRST TO DELETE")
            return

        confirm_deletion = messagebox.askyesno("CONFIRM DELETION?", "ARE YOU SURE YOU WANT TO DELETE THIS PLAYER?")
        if not confirm_deletion:
            return

        deleted_record = self.player_db.delete_player(self.current_user, self.selected_player_id)

        if deleted_record:
            messagebox.showinfo("SUCCESS", "PLAYER DELETED SUCCESSFULLY")
            self.search_player()
            self.selected_player_id = None

        else:
            messagebox.showerror("ERROR", "PLAYER DELETION FAILED")


    def go_back(self):
        self.window.destroy()
        self.parent.deiconify()

