from bff.models import Account, Match
from bff.database import AccountDB, MatchDB

# #CREATE DATABASE INSTANCE
# account_db = AccountDB()
# #TEST DATA
# username = "test_user01"
# password = "password123"
#
# #HASH PASSWORD
# hashed_password = Account.hash_password(password)
#
# #TEST 1
# created = account_db.create_account(username, hashed_password)
# print("ACCOUNT CREATED:", created)
#
# #TEST 2
# account_doc = account_db.find_account(username)
# print("ACCOUNT FOUND:", account_doc is not None)
#
# #TEST 3
# if account_doc:
#     print("STORED USERNAME:", account_doc["username"])
#
# #TEST 4
# duplicate_account = account_db.create_account(username, hashed_password)
# print("ACCOUNT CREATED", duplicate_account)
#


# #TEST 4
# if account_doc:
#     account_obj = Account.from_dict(account_doc)
#     is_correct = Account.verify_password(password, account_obj.hashed_password)
#     print("Password Verified:", is_correct)




#Create instance of MatchDB
match_db = MatchDB()

#Dummy match data
dummy_match = {
    "match_date": "2026-02-25",
    "match_format": "T20",
    "match_type": "Friendly",
    "venue": "Home",
    "ground_name": "Edgbaston",
    "opposition": "India",
    "result": "Win",
    "toss_result": "WON_BAT",
    "team_players": [],
    "batting_scorecard": [],
    "bowling_scorecard": [],
    "fielding_scorecard": []
}

#Call create_match method
inserted_id = match_db.create_match("test_user01", dummy_match)

#Print result
if inserted_id:
    print("Match inserted successfully.")
    print("MATCH ID:", inserted_id)
else:
    print("Match insertion failed.")