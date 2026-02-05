import tkinter as tk

from gui.baseWindow import BaseWindow
from gui.match import CreateMatchDetailsPage, SelectTeamPage, MatchScorecard
from gui.start import StartWindow

root=tk.Tk()
StartWindow(root)
#MatchScorecard(root, SelectTeamPage, "kaushal", match_id="", team_data="")
root.mainloop()