from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
load_dotenv()
MONGO_DETAILS = os.getenv("MONGO_URL")
print(MONGO_DETAILS)
client: AsyncIOMotorClient = None


async def connect_to_mongo():
    global client
    client = AsyncIOMotorClient(MONGO_DETAILS)
    print("Connected to MongoDB")
    print(MONGO_DETAILS)


async def close_mongo_connection():
    global client
    if client:
        client.close()
        print("Closed connection to MongoDB")

async def get_database():
    global client
    if not client:
        await connect_to_mongo()
    print("came in getting database")
    return client["FastApi"]  # Access the 'FastApi' database

async def get_collection(collection_name: str):
    db = await get_database()
    return db[collection_name]  # Access the specified collection
