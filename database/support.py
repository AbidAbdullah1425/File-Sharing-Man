import asyncio
from pymongo import MongoClient
from pyrogram.errors import FloodWait
from config import DB_URI

client = MongoClient(DB_URI)
db = client["Cluster0"]
collection = db["broadcast"]

async def query_msg():
    """Fetch user IDs from MongoDB."""
    return [doc["_id"] for doc in collection.find({}, {"_id": 1})]

async def users_info(bot):
    users = 0
    blocked = 0
    identity = await query_msg()
    for user_id in identity:
        name = False
        try:
            name = await bot.send_chat_action(int(user_id), "typing")
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except Exception:
            pass
        if name:
            users += 1
        else:
            blocked += 1
    return users, blocked
