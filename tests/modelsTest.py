from bff.classModels import (Match)

from datetime import datetime

#key

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
        "bowling": [{"player_id": "id-01", "player_name": "name_test01"}],
        "fielding": []
}
}
match_test01 = Match.from_database(dummy_match)

print(match_test01.scorecard.batting[0].runs_scored)

print(match_test01.scorecard.batting[0].how_out)

print(match_test01.scorecard.bowling[0].player_name)

print(match_test01.match_date)

