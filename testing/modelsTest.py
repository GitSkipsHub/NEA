import bcrypt
from bff.models import (Account, Player, Match)

#
# #TEST 1: CHECK IF HASH PASSWORD FUNCTION IS WORKING
# password = "test_password01"
# hashed_password = Account.hash_password(password)
#
# #CREATED DUMMY ACCOUNT OBJECT
# dummy_account = Account(
#     username="username01",
#     hashed_password=hashed_password
# )
#
# #TEST 2: CONVERT ACCOUNT OBJECT TO DICT
# account_dict = dummy_account.to_dict()
# print(f"ACCOUNT DICT: \n    {account_dict}")
#
# #TEST 3: CONVERT ACCOUNT DICT TO OBJECT
# account_obj = dummy_account.from_dict(account_dict)
# print(f"\nACCOUNT OBJECT --> \n  {account_obj}")
# print(f"\nHASHED PASSWORD = {account_obj.hashed_password}")
# print(f"\nUSERNAME = {account_obj.username}")
#
# #TEST 4
# correct_password = bcrypt.checkpw("test_password01".encode("utf-8"), account_obj.hashed_password.encode("utf-8"))
# print(f"\nCORRECT PASSWORD: {correct_password}")
#
# #TEST 5
# wrong_password = bcrypt.checkpw("wrong_password".encode("utf-8"), account_obj.hashed_password.encode("utf-8"))
# print(f"\nWRONG PASSWORD: {wrong_password}\n")
#
# #TEST 6
# #print(Account.from_dict({}))
#

#CREATED DUMMY PLAYER OBJECT
dummy_player = Player(
    player_id="pId01",
    username="username01",
    first_name="Virat",
    last_name="Kohli",
    date_of_birth="1988-11-05",
    player_role="BATTER",
    batting_style="RIGHT_HAND",
    bowling_style="RAP"
)

#TEST 1
player_dict = dummy_player.to_dict()
for key, value in player_dict.items():
    print(f"PLAYER DICT --> {key}: {value}")


# #CREATED DUMMY PLAYER OBJECT
# dummy_player = Player(
#     player_id="temp_id", #not stored in Mongo as MongoDB uses _id
#     username="username01",
#     first_name="Virat",
#     last_name="Kohli",
#     date_of_birth="1988-11-05",
#     player_role="BATTER",
#     batting_style="RIGHT_HAND",
#     bowling_style="RAP"
# )
#
# #TEST 1
# player_dict = dummy_player.to_dict()
# for key, value in player_dict.items():
#     print(f"PLAYER DICT --> {key}: {value}")
#
# #TEST 2
# fake_mongo_player = player_dict.copy()
# fake_mongo_player["_id"] = "507f1f77bcf86cd799439011"
#
# #TEST 3
# player_obj = Player.from_dict(fake_mongo_player)
# print(f"\nplayer_id = {player_obj.player_id}")
# print(f"\nusername = {player_obj.username}")
# print(f"\nfull_name = {player_obj.first_name} {player_obj.last_name}\n")



#CREATED DUMMY SCORECARDS
batting_scorecard = [
    {
        "player_id": "p1",
        "position": 1,
        "player_name": "player01",
        "player_role": "BATTER",
        "batting_style": "RH",
        "how_out": "CAUGHT",
        "fielder": "player02",
        "bowler": "player03",
        "runs_scored": 45,
        "balls": 32,
        "fours": 6,
        "sixes": 1,
    },
]

bowling_scorecard = [
    {
        "player_id": "p3",
        "position": 1,
        "player_name": "player05",
        "player_role": "BOWLER",
        "bowling_style": "RAP",
        "overs": 4.0,
        "maidens": 0,
        "runs_conceded": 22,
        "wickets": 2,
        "wides": 1,
        "no_balls": 0,
    },
]

fielding_scorecard = [
    {
        "player_id": "p5",
        "position": 1,
        "player_name": "player07",
        "player_role": "WKT_KEEPER",
        "batting_style": "RH",
        "catches": 1,
        "runouts": 0,
        "stumpings": 1,
    },
]

batting_summary = {"subtotal": 75, "extras": 10, "total": 85}
fielding_extras = {"byes": 2, "leg_byes": 1, "penalties": 0}

#CREATED DUMMY MATCH
dummy_match = Match(
    match_id="TEMP_ID",  #not stored in Mongo (Mongo uses _id)
    username="username_01",
    match_date="2025-08-12",
    match_format="T20",
    match_type="LEAGUE",
    venue="HOME",
    ground_name="Ground 1",
    opposition="Oppo 1",
    result="WON",
    toss_result="WON_BAT",
    team_players=[
        {"player_id": "mongo_id01", "position": 1, "player_name": "player01",},
        {"player_id": "mongo_id02", "position": 2, "player_name": "player02",},
        {"player_id": "mongo_id03", "position": 3, "player_name": "player03",}
    ],
    batting_scorecard=batting_scorecard,
    bowling_scorecard=bowling_scorecard,
    fielding_scorecard=fielding_scorecard,
    batting_summary=batting_summary,
    fielding_extras=fielding_extras,
    captain_id="p1",
    wk_id="p2"
)

#TEST 1
match_dict = dummy_match.to_dict()
for key, value in match_dict.items():
    print(f"MATCH DICT --> {key}: {value}")

#TEST 2
fake_mongo_match = match_dict.copy()
fake_mongo_match["_id"] = "65ab3f4e9b1c2d3e4f5a6789"

#TEST 3
match_obj = Match.from_dict(fake_mongo_match)
print(f"\nmatch_id = {match_obj.match_id}")
print(f"username = {match_obj.username}")
print(f"match_format = {match_obj.match_format}")
print(f"match_type = {match_obj.match_type}")
print(f"team_players = {match_obj.team_players}")
print(f"batting_scorecard = {match_obj.batting_scorecard}")
