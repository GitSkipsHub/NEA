from bff.models import (Match, Account, TeamGenerator)

from datetime import datetime

from bff.enums import TimePeriod

#key

#CREATED DUMMY ACCOUNT
dummy_account = {
    "username": "username-test01",
    "password": "password-test01",
    "hashed_password": ""
}
#Returns all the values stored in Account Object as strings
account_test01 = Account.from_database(dummy_account)
#Assigns password in dummy_account dict to attribute password in Account Class
password = account_test01.password
#Hashes Password Method
hashed_password = Account.hash_password(password)
#Prints Password & Hashed Password
print(f'Password = {password} | Hashed Password = {hashed_password}')



#CREATED DUMMY MATCH
dummy_match = {
    "username": "username01",
    "match_id": "id-01",
    "match_date": datetime.now(),
    "match_format": "T20",
    "match_type": "LEAGUE",
    "venue": "HOME",
    "opposition": "England",
    "ground_name": "Oval",
    "toss": "WON_BAT",
    "result": "LOST",
    "period": "LAST_MONTH",
    "scorecard": {
        "batting": [{"player_id": "id-01", "player_name": "name_test01",
                     "runs_scored": 50, "how_out": "BOWLED", }],
        "bowling": [{"player_id": "id-01", "player_name": "name_test01",
                     "overs": 23.4, "maidens": 3, "wickets": 5}],
        "fielding": []
}
}
#Returns all the values stored in Match Object as strings
match_test01 = Match.from_database(dummy_match)
#Returns runs scored from Scorecard Dictionary & Batting List
print(match_test01.scorecard.batting[0].runs_scored)
#Returns Dismissal Type
print(match_test01.scorecard.batting[0].how_out)
#Returns player_name in the match
print(match_test01.scorecard.bowling[0].player_name)
#Returns no.overs
print(match_test01.scorecard.bowling[0].overs)
#Returns no.wickets
print(match_test01.scorecard.bowling[0].wickets)
#Returns data created
print(match_test01.match_date)



#CREATED INVALID TEAM COMPOSITION
team_gen = TeamGenerator(
    time_period= TimePeriod.LAST_MONTH,
    no_of_batters=3,
    no_of_pacers=2,
    no_of_spinners=2,
    no_of_all_rounders=2,
    no_of_wicketkeepers=1
    )

result = TeamGenerator.validate_team_composition(team_gen)
print(f"INVALID TEAM COMPOSITION --> {result}")

#CREATED VALID & UNBALANCED TEAM COMPOSITION
team_gen = TeamGenerator(
    time_period= TimePeriod.LAST_MONTH,
    no_of_batters=4,
    no_of_pacers=2,
    no_of_spinners=2,
    no_of_all_rounders=2,
    no_of_wicketkeepers=1
)

result = TeamGenerator.validate_team_composition(team_gen)
print(f"VALID & UNBALANCED TEAM COMPOSITION --> {result}")


#CREATED VALID & BALANCED TEAM COMPOSITION
team_gen = TeamGenerator(
    time_period= TimePeriod.LAST_MONTH,
    no_of_batters=4,
    no_of_pacers=1,
    no_of_spinners=2,
    no_of_all_rounders=3,
    no_of_wicketkeepers=1
)

result = TeamGenerator.validate_team_composition(team_gen)
print(f"VALID & UNBALANCED TEAM COMPOSITION --> {result}")




