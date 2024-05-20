from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

MONGO_DETAILS = "mongodb://localhost:27017"

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.property_management

property_collection = database.get_collection("properties")

def property_helper(property) -> dict:
    return {
        "id": str(property["_id"]),
        "name": property["name"],
        "address": property["address"],
        "city": property["city"],
        "state": property["state"],
    }
