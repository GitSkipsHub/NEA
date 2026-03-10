import tkinter as tk

from gui.baseWindow import BaseWindow
from gui.match import CreateMatchDetailsPage, SelectTeamPage, MatchScorecard, MatchManagementPage
from gui.start import StartWindow

root=tk.Tk()
#StartWindow(root)
#CreateMatchDetailsPage(root, MatchManagementPage, "kaushal")
#MatchScorecard(root, SelectTeamPage, "kaushal", match_id="", selected_team="")
SelectTeamPage(root, CreateMatchDetailsPage, "kaushal", created_match_id="")


#MatchScorecard(root, root, "kaushal", match_id="69a317738093e6761e48348e")

root.mainloop()