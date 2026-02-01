from bson.errors import InvalidId
from pymongo import mongo_client, MongoClient
from pymongo.errors import ConnectionFailure, DuplicateKeyError, PyMongoError
from datetime import datetime
from typing import Optional, List, Dict
from bson.objectid import ObjectId

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

    def create_player(self, username: str, player_data: Dict) -> bool:
        try:
            player_data["username"] = username
            player_data["created_date"] = datetime.now()
            player_data["last_updated"] = datetime.now()

            stats_fields = ["matches", "innings", "runs_scored", "balls", "fours",
                            "sixes", "wickets", "overs", "maidens", "runs_given",
                            "wides", "no_balls", "catches","runouts", "stumpings"]

            for field in stats_fields:
                if field not in player_data:
                    player_data[field] = 0

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
            return result.matched_count == 1
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

    def update_match(self):
        pass





