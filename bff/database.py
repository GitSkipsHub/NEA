from bson.errors import InvalidId
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, DuplicateKeyError, PyMongoError
from datetime import datetime
from typing import Optional, List, Dict, Any
from bson.objectid import ObjectId

#client = MongoClient("mongodb://localhost:27017/")

#DB NAME
my_db = "smart_skipper_db"

#Local Host URI
mongo_db_uri = "mongodb://localhost:27017/"
client = MongoClient('mongodb://localhost:27017/')

class Database:
    #Initialise all as None
    instance = None
    client = None
    db = None

    #Creates New Database if Instance = None
    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(Database, cls).__new__(cls)
            cls.instance.client = None
            cls.instance.db = None
        return cls.instance

    #Calls Connect function if client = None
    def __init__(self):
        if self.client is None:
            self.connect()

    #Connect Database Function
    def connect(self):
        try:
            self.client = MongoClient(mongo_db_uri)
            self.db = self.client[my_db]
            #Ping Test --> Checks if Database is up-and-running
            self.client.admin.command("ping")
            print("Successfully connected to MongoDB")

        except ConnectionFailure as e:
            print(f"Failed to connect to MongoDB as {e}")
            raise

    #Gets Tables stored within Database (e.g. Account)
    def get_collection(self, collection_name: str):
        return self.db[collection_name]

    #Closes Connection to Database
    def close(self):
        if self.client:
            self.client.close()
            print("Database connection closed")

class AccountDB:

    def __init__(self):
        self.db = Database()
        self.collection = self.db.get_collection("account")

    def create_account(self, username: str, hashed_password: str):
        try:
            account = {
                "username": username,
                "hashed_password": hashed_password,
                "created_date": datetime.now()
            }
            result = self.collection.insert_one(account)
            #This is used to  return True only if MongoDB confirms the document was successfully inserted
            return result is not None #insert id is None is insert failed
        #Prevents Duplicate Accounts Created
        except DuplicateKeyError:
            return False

    #Self Explanatory - Finds Account
    def find_account(self, username: str) -> Optional[Dict]:
        return self.collection.find_one({"username": username})

    def username_exists(self, username: str) -> Optional[Dict]:
        return self.collection.find_one({"username": username})is not None
        #Returns True if account found and False is account not found
        #Account is not None = True | None is not None = False

class PlayerDB:

    def __init__(self):
        self.db = Database()
        self.collection = self.db.get_collection("player")

    def create_player(self, username: str, player_data: Dict):
        try:
            player_data["username"] = username
            player_data["created_date"] = datetime.now()
            player_data["last_updated"] = datetime.now()

            stats_fields_defaults = {
                "matches": 0, "innings": 0, "runs_scored": 0, "balls": 0, "fours": 0,
                "sixes": 0, "overs": 0,"maidens": 0, "runs_conceded": 0, "wickets": 0, "wides": 0,
                "no_balls": 0, "catches": 0, "runouts": 0, "stumpings": 0,
            }

            for j, k in stats_fields_defaults.items():
                player_data.setdefault(j, k)

            result = self.collection.insert_one(player_data)
            return result.inserted_id is not None

        except Exception as e:
            print(f"Error creating Player: {e}")

    def search_player(self, username, search_term: str = "") -> List[Dict]:
        search_term = search_term.strip() #Removes whitespaces
        query = {"username": username} #Restricts mongo query to players within that profile
        if search_term:
            query["$or"] = [
                {"first_name": {"$regex": search_term, "$options": "i"}}, #Finds value matching regular expression where option = case-insensitive
                {"last_name": {"$regex": search_term, "$options": "i"}}
            ]
        return list(self.collection.find(query).sort("last_name", 1))

    def get_all_players(self, username: str) -> List[Dict]:
        return list(self.collection.find({"username": username}))

    def update_player(self, username: str, player_id, update_data):
        try:
            update_data["last_updated"] = datetime.now()
            result = self.collection.update_one(
                {"username": username, "_id": ObjectId(player_id)},
                {"$set": update_data}
            )
            return result.modified_count == 1
        except InvalidId:
            return False
        except PyMongoError as e:
            print(f"Database error updating {e}")
            return False

    def delete_player(self, username: str, player_id: str) -> bool:
        try:
            result = self.collection.delete_one({
                "username": username,
                "_id": ObjectId(player_id)
            })
            return result.deleted_count == 1
        except Exception as e:
            print(f"Error deleting player {e}")
            return False

class MatchDB:
    def __init__(self):
        self.db = Database()
        self.collection = self.db.get_collection("match")

    def create_match(self, username: str, match_data: Dict) -> Optional[str]:
        try:
            match_data["username"] = username
            match_data["created_date"] = datetime.now()
            match_data["last_updated"] = datetime.now()
            result = self.collection.insert_one(match_data)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error creating match {e}")
            return None

    def update_match(self, username: str, match_id, update_data):
        try:
            update_data["last_updated"] = datetime.now()
            result = self.collection.update_one(
                {"username": username, "_id": ObjectId(match_id)},
                {"$set": update_data}
            )
            return result.modified_count == 1
        except InvalidId:
            return False
        except PyMongoError as e:
            print(f"Database error as {e}")
            return False

    def search_match(self, username: str, filters: Dict[str, Any] ) -> List[Dict]:
        query: Dict[str, Any] = {"username": username}

        if filters.get("match_date"):
            query["match_date"] = filters["match_date"]
        if filters.get("venue"):
            query["venue"] = filters["venue"]
        if filters.get("result"):
            query["result"] = filters["result"]
        if filters.get("match_type"):
            query["match_type"] = filters["match_type"]
        if filters.get("match_format"):
            query["match_format"] = filters["match_format"]
        if filters.get("opposition"):
            query["opposition"] = {"$regex" : filters["opposition"],"$options": "i"}

        return list(self.collection.find(query).sort("match_date", -1))

    def find_match(self, username: str, match_id: str):
        try:
            return self.collection.find_one(
                {"username": username, "_id": ObjectId(match_id)}
            )
        except InvalidId:
            return None

    def get_all_matches(self, username:str) -> List[Dict]:
        return list(self.collection.find({"username": username}))

    def delete_match(self, username: str, match_id: str) -> bool:
        try:
            result = self.collection.delete_one(
                {"username": username, "_id": ObjectId(match_id)}
            )
            return result.deleted_count == 1
        except Exception as e:
            print(f"Error deleting match {e}")
            return False

class TeamGeneratorDB:
    def __init__(self):
        self.db = Database()
        self.collection = self.db.get_collection("match")

    def generate_team(self, username: str, match_type: str, match_format: str, venue: str, from_date: datetime,
                      batter_limit: int, pacer_limit: int, spinner_limit: int, all_rounder_limit: int, wk_limit: int):

        limits = [batter_limit, pacer_limit, spinner_limit, all_rounder_limit, wk_limit]
        if any(type(x) is not int for x in limits) or any(x < 0 for x in limits):
            raise ValueError ("Limits must be positive integers")

        pipeline = [
            {
                '$addFields': {
                    'match_date_dt': {
                        '$dateFromString': {
                            'dateString': '$match_date',
                            'format': '%Y-%m-%d',
                            'timezone': 'Europe/London'
                        }
                    }
                }
            }, {
                '$match': {
                    'username': username,
                    'venue': venue,
                    'match_type': match_type,
                    'match_format': match_format,
                    'match_date_dt': {
                        '$gte': from_date
                    }
                }
            }, {
                '$facet': {
                    'batters': [
                        {
                            '$unwind': '$batting_scorecard'
                        }, {
                            '$match': {
                                'batting_scorecard.player_role': 'BATTER'
                            }
                        }, {
                            '$group': {
                                '_id': '$batting_scorecard.player_id',
                                'player_name': {
                                    '$first': '$batting_scorecard.player_name'
                                },
                                'total_runs': {
                                    '$sum': '$batting_scorecard.runs_scored'
                                },
                                'player_role': {
                                    '$first': '$batting_scorecard.player_role'
                                }
                            }
                        }, {
                            '$sort': {
                                'total_runs': -1
                            }
                        }, {
                            '$limit': batter_limit
                        }, {
                            '$project': {
                                '_id': 0,
                                'player_name': 1,
                                'player_role': 1,
                                'total_runs': 1,
                                'player_id': '$_id'
                            }
                        }
                    ],
                    'pacers': [
                        {
                            '$unwind': '$bowling_scorecard'
                        }, {
                            '$match': {
                                'bowling_scorecard.player_role': 'BOWLER',
                                'bowling_scorecard.bowling_style': {
                                    '$in': [
                                        'RAP', 'LAP'
                                    ]
                                }
                            }
                        }, {
                            '$group': {
                                '_id': '$bowling_scorecard.player_id',
                                'player_name': {
                                    '$first': '$bowling_scorecard.player_name'
                                },
                                'player_role': {
                                    '$first': '$bowling_scorecard.player_role'
                                },
                                'total_wickets': {
                                    '$sum': '$bowling_scorecard.wickets'
                                }
                            }
                        }, {
                            '$sort': {
                                'total_wickets': -1
                            }
                        }, {
                            '$limit': pacer_limit
                        }, {
                            '$project': {
                                '_id': 0,
                                'player_id': '$_id',
                                'player_name': 1,
                                'player_role': 1,
                                'total_wickets': 1
                            }
                        }
                    ],
                    'spinners': [
                        {
                            '$unwind': '$bowling_scorecard'
                        }, {
                            '$match': {
                                'bowling_scorecard.player_role': 'BOWLER',
                                'bowling_scorecard.bowling_style': {
                                    '$in': [
                                        'RAOS', 'LAOS', 'RALS', 'LALS'
                                    ]
                                }
                            }
                        }, {
                            '$group': {
                                '_id': '$bowling_scorecard.player_id',
                                'player_name': {
                                    '$first': '$bowling_scorecard.player_name'
                                },
                                'player_role': {
                                    '$first': '$bowling_scorecard.player_role'
                                },
                                'total_wickets': {
                                    '$sum': '$bowling_scorecard.wickets'
                                }
                            }
                        }, {
                            '$sort': {
                                'total_wickets': -1
                            }
                        }, {
                            '$limit': spinner_limit
                        }, {
                            '$project': {
                                '_id': 0,
                                'player_id': '$_id',
                                'player_name': 1,
                                'player_role': 1,
                                'total_wickets': 1
                            }
                        }
                    ],
                    'all_rounders': [
                        {
                            '$project': {
                                'ar_events': {
                                    '$concatArrays': [
                                        {
                                            '$map': {
                                                'input': {
                                                    '$filter': {
                                                        'input': '$batting_scorecard',
                                                        'as': 'b',
                                                        'cond': {
                                                            '$eq': [
                                                                '$$b.player_role', 'ALL_ROUNDER'
                                                            ]
                                                        }
                                                    }
                                                },
                                                'as': 'batter',
                                                'in': {
                                                    'player_id': '$$batter.player_id',
                                                    'player_name': '$$batter.player_name',
                                                    'player_role': '$$batter.player_role',
                                                    'runs': '$$batter.runs_scored'
                                                }
                                            }
                                        }, {
                                            '$map': {
                                                'input': {
                                                    '$filter': {
                                                        'input': '$bowling_scorecard',
                                                        'as': 'w',
                                                        'cond': {
                                                            '$eq': [
                                                                '$$w.player_role', 'ALL_ROUNDER'
                                                            ]
                                                        }
                                                    }
                                                },
                                                'as': 'bowler',
                                                'in': {
                                                    'player_id': '$$bowler.player_id',
                                                    'player_name': '$$bowler.player_name',
                                                    'player_role': '$$bowler.player_role',
                                                    'wickets': '$$bowler.wickets'
                                                }
                                            }
                                        }
                                    ]
                                }
                            }
                        }, {
                            '$unwind': '$ar_events'
                        }, {
                            '$group': {
                                '_id': '$ar_events.player_id',
                                'player_name': {
                                    '$first': '$ar_events.player_name'
                                },
                                'total_runs': {
                                    '$sum': '$ar_events.runs'
                                },
                                'total_wickets': {
                                    '$sum': '$ar_events.wickets'
                                },
                                'player_role': {
                                    '$first': '$ar_events.player_role'
                                }
                            }
                        }, {
                            '$sort': {
                                'total_runs': -1,
                                'total_wickets': -1
                            }
                        }, {
                            '$limit': all_rounder_limit
                        }, {
                            '$project': {
                                '_id': 0,
                                'player_id': '$_id',
                                'player_name': 1,
                                'player_role': 1,
                                'total_runs': 1,
                                'total_wickets': 1
                            }
                        }
                    ],
                    'wicket_keepers': [
                        {
                            '$project': {
                                'wk_events': {
                                    '$concatArrays': [
                                        {
                                            '$map': {
                                                'input': {
                                                    '$filter': {
                                                        'input': '$batting_scorecard',
                                                        'as': 'b',
                                                        'cond': {
                                                            '$eq': [
                                                                '$$b.player_role', 'WKT_KEEPER'
                                                            ]
                                                        }
                                                    }
                                                },
                                                'as': 'batter',
                                                'in': {
                                                    'player_id': '$$batter.player_id',
                                                    'player_name': '$$batter.player_name',
                                                    'player_role': '$$batter.player_role',
                                                    'runs': '$$batter.runs_scored'
                                                }
                                            }
                                        }, {
                                            '$map': {
                                                'input': {
                                                    '$filter': {
                                                        'input': '$fielding_scorecard',
                                                        'as': 'f',
                                                        'cond': {
                                                            '$eq': [
                                                                '$$f.player_role', 'WKT_KEEPER'
                                                            ]
                                                        }
                                                    }
                                                },
                                                'as': 'wk',
                                                'in': {
                                                    'player_id': '$$wk.player_id',
                                                    'player_name': '$$wk.player_name',
                                                    'player_role': '$$wk.player_role',
                                                    'catches': '$$wk.catches',
                                                    'runouts': '$$wk.runouts',
                                                    'stumpings': '$$wk.stumpings'
                                                }
                                            }
                                        }
                                    ]
                                }
                            }
                        }, {
                            '$unwind': '$wk_events'
                        }, {
                            '$group': {
                                '_id': '$wk_events.player_id',
                                'player_name': {
                                    '$first': '$wk_events.player_name'
                                },
                                'total_runs': {
                                    '$sum': '$wk_events.runs'
                                },
                                'total_dismissals': {
                                    '$sum': {
                                        '$add': [
                                            '$wk_events.catches', '$wk_events.runouts', '$wk_events.stumpings'
                                        ]
                                    }
                                },
                                'player_role': {
                                    '$first': '$wk_events.player_role'
                                }
                            }
                        }, {
                            '$sort': {
                                'total_runs': -1,
                                'total_dismissals': -1
                            }
                        }, {
                            '$limit': wk_limit
                        }, {
                            '$project': {
                                '_id': 0,
                                'player_id': '$_id',
                                'player_name': 1,
                                'player_role': 1,
                                'total_runs': 1,
                                'total_dismissals': 1
                            }
                        }
                    ]
                }
            }, {
                '$project': {
                    'combined': {
                        '$concatArrays': [
                            '$batters', '$wicket_keepers', '$all_rounders', '$spinners', '$pacers',
                        ]
                    }
                }
            }, {
                '$unwind': '$combined'
            }, {
                '$replaceRoot': {
                    'newRoot': '$combined'
                }
            }
        ]

        result = list(self.collection.aggregate(pipeline))
        return result