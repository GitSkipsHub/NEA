from platformdirs import user_log_dir
from pymongo import mongo_client, MongoClient
from typing import Dict, List, Optional
from datetime import datetime

db_uri = "mongodb://localhost:27017/"

db_name = "smart_skipper_db"

class Database:

    instance = None
    client = None
    db = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(Database, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        if self.client is None:
            self.connect()

    def connect(self):
        try:
            self.client = MongoClient(db_uri)
            self.db = self.client[db_name]
            self.client.admin.command("ping")
            print("Successfully connected to MongoDB")
        except Exception as e:
            print(f"Failed to connect to MongoDB {e}")
            raise

    def get_collection(self, collection_name: str):
        return self.db[collection_name]

    def close(self):
        if self.client:
            self.client.close()
            print("Database connection closed")


class AccountDB:

    def __init__(self):
        self.db = Database()
        self.collection = self.db.get_collection("account")

    def create_account(self, username: str, hashed_password: str) -> bool:
        try:
            account = {
                "username": username,
                "hashed_password": hashed_password,
                "created_date": datetime.now()
            }
            self.collection.insert_one(account)
            return True
        except:
            return False

    def find_account(self, username: str) -> bool:
        return self.collection.find_one({"username": username})

    def username_exists(self, username: str) -> bool:
        return self.collection.find_one({"username": username})

class PlayerDB:

    def __init__(self):
        self.db = Database()
        self.collection = self.db.get_collection("player")










