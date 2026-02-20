from datetime import datetime
from bff.models import (Match, Player, Account)


#CREATED DUMMY ACCOUNT
dummy_account = {
    "username": "username-test01",
    "hashed_password": ""
}
#Returns all the values stored in Account Object as strings
account = Account.from_dict(dummy_account)

assert account.username == "username-test01"

password = "password_test01"

hashed_password = Account.hash_password(password)

if Account.verify_password("password_test01", hashed_password):
    print("PASS")


assert hashed_password != password

print("ACCOUNT TEST PASSED")

print(f'Password = {password} | Hashed Password = {hashed_password}')


# dummy_player = {
#     "username": "dummy_username",
#     "player_id": "01",
#     "first_name": "dummy_first_name",
#     "last_name": "dummy_last_name",
#     "date_of_birth": "dummy_dob",
#     "player_role": "BATTER",
#     "batting_style": "LEFT_HAND",
#     "bowling_style":"LEFT_ARM_PACE",
# }
#
#
# player_test01 = Player.from_dict(dummy_player)
#
# print(player_test01.username)
# print(player_test01.player_role)
#
#
#
# #CREATED DUMMY MATCH
# dummy_match = {
#     "username": "username01",
#     "match_id": "id-01",
#     "match_date": datetime.now(),
#     "match_format": "T20",
#     "match_type": "LEAGUE",
#     "venue": "HOME",
#     "opposition": "England",
#     "ground_name": "Oval",
#     "toss": "WON_BAT",
#     "result": "LOST",
#     "scorecard": {"subtotal": 100, "extras": 50, "total": 150, "byes_conceded": 20, "leg_byes_conceded": 30,
#                   "penalties_conceded": 0, "batting_overs": 20, "bowling_overs": 18,
#
#         "batting": [{"player_id": "id-01", "player_name": "name_test01", "pos": 1,
#                      "how_out": "BOWLED", "fielder": "mid-off", "bowler": "Bowler No.1",
#                      "runs_scored": 50, "balls": 50, "fours": 3, "sixes": 0 }],
#
#         "bowling": [{"player_id": "id-01", "player_name": "name_test01", "pos": 1,
#                      "overs": 23.4, "maidens": 3, "runs_conceded": 95, "wickets": 5, "wides": 4, "no_balls": 0}],
#
#         "fielding": []
# }
# }
# #Returns all the values stored in Match Object as strings
# match_test01 = Match.from_dict(dummy_match)
# #Returns runs scored from Scorecard Dictionary & Batting List
# print(match_test01.batting[0].runs_scored)
# #Returns Dismissal Type
# print(match_test01.scorecard.batting[0].how_out)
# #Returns player_name in the match
# print(match_test01.scorecard.bowling[0].player_name)
# #Returns no.overs
# print(match_test01.scorecard.bowling[0].overs)
# #Returns no.wickets
# print(match_test01.scorecard.bowling[0].wickets)
# #Returns data created
# print(match_test01.match_date)
#
#
#
#
