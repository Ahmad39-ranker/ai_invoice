# database/db.py
from motor.motor_asyncio import AsyncIOMotorClient
from config.settings import settings

class Database:
    def __init__(self):
        self.client = AsyncIOMotorClient(settings.MONGO_URI)
        self.db = self.client[settings.MONGO_DB_NAME]

db = Database()