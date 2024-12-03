import threading
from pymongo import MongoClient
import os

DB_URI = os.environ.get("DATABASE_URI", "your_mongodb_connection_string")
client = MongoClient(DB_URI)
db = client["Cluster0"]
broadcast_collection = db["broadcast"]

INSERTION_LOCK = threading.RLock()

# Add user details
async def add_user(id, user_name):
    with INSERTION_LOCK:
        if not broadcast_collection.find_one({"_id": id}):
            broadcast_collection.insert_one({"_id": id, "user_name": user_name})

# Delete user details
async def delete_user(id):
    with INSERTION_LOCK:
        broadcast_collection.delete_one({"_id": id})

# Get all user details
async def full_userbase():
    with INSERTION_LOCK:
        users = list(broadcast_collection.find({}, {"_id": 1, "user_name": 1}))
    return users

# Query user IDs
async def query_msg():
    with INSERTION_LOCK:
        users = list(broadcast_collection.find({}, {"_id": 1}).sort("_id"))
    return users
