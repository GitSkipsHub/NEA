import tkinter as tk

from gui.baseWindow import BaseWindow
from gui.match import CreateMatchDetailsPage, SelectTeamPage, MatchScorecard, MatchManagementPage
from gui.start import StartWindow

root=tk.Tk()
StartWindow(root)
#CreateMatchDetailsPage(root, MatchManagementPage, "kaushal")
#MatchScorecard(root, SelectTeamPage, "kaushal", match_id="", selected_team="")
#SelectTeamPage(root, CreateMatchDetailsPage, "kaushal", created_match_id="")

# dummy_team = {
#     "team_players": [
#         {"player_id": "1", "position": 1, "player_name": "Player 1"},
#         {"player_id": "2", "position": 2, "player_name": "Player 2"},
#         {"player_id": "3", "position": 3, "player_name": "Player 3"},
#         {"player_id": "4", "position": 4, "player_name": "Player 4"},
#         {"player_id": "5", "position": 5, "player_name": "Player 5"},
#         {"player_id": "6", "position": 6, "player_name": "Player 6"},
#         {"player_id": "7", "position": 7, "player_name": "Player 7"},
#         {"player_id": "8", "position": 8, "player_name": "Player 8"},
#         {"player_id": "9", "position": 9, "player_name": "Player 9"},
#         {"player_id": "10", "position": 10, "player_name": "Player 10"},
#         {"player_id": "11", "position": 11, "player_name": "Player 11"},
#     ],
#     "captain_id": "1",
#     "wk_id": "2"
# }
# MatchScorecard(root, root, "kaushal", match_id="123", selected_team=dummy_team)

root.mainloop()