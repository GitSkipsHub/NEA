from pymongo import mongo_client, MongoClient

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

    def close(self):
        if self.client:
            self.client.close()
            print("Database connection closed")





