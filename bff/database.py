from pymongo import mongo_client, MongoClient

client = MongoClient("mongodb://localhost:27017/")

my_db = client["smart_skipper_db"]


