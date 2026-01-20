from pymongo import mongo_client, MongoClient
from pymongo.errors import ConnectionFailure, DuplicateKeyError
from datetime import datetime
from typing import Optional, List, Dict

#client = MongoClient("mongodb://localhost:27017/")

#DB NAME
my_db = "smart_skipper_db"

#Local Host URI
mongo_db_uri = "mongodb://localhost:27017/"


class Database:
    #Initialise all as None
    instance = None
    client = None
    db = None

    #Creates New Database if Instance = None
    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(Database, cls).__new__(cls)
        return cls.instance

    #Calls Connect function if client = None
    def __init__(self):
        self.client = None
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
            self.collection.insert_one(account)
            return True
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

    def create_player(self, username: str, player_data: Dict) -> bool:
        try:
            player_data["username"] = username,
            player_data["created_date"] = datetime.now(),
            player_data["last_updated"] = datetime.now()

            stats_fields = ["matches", "innings", "runs_scored", "balls", "fours",
                            "sixes", "wickets", "overs", "maidens", "runs_given",
                            "wides", "no_balls", "catches","runouts", "stumpings"]
            for field in stats_fields:
                player_data[field] = 0

            result = self.collection.insert_one(player_data)
            return result.__inserted_id is not None

        except Exception as e:
            print(f"Error creating Player: {e}")








