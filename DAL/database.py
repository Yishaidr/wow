import motor.motor_asyncio
from bson.objectid import ObjectId


MONGO_DETAILS = "mongodb://wowmongo:27017"

wow= motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = wow.schedule


def event_helper(event) -> dict:
    return {
        "date": event["date"],
        "title": event["title"],
        "email": event["relevant"]
    }


async def retrieve_schedule(schedule):
    events = []
    events_collection = database.get_collection(schedule)
    async for event in events_collection.find():
        events.append(event_helper(event))
    return events