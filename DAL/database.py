import motor.motor_asyncio
from bson.objectid import ObjectId


MONGO_DETAILS = "mongodb://admin:wowisofek@wowmongo.eastus.azurecontainer.io:27017"

wow= motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = wow.schedule


def event_helper(event) -> dict:
    return {
        "time": event["time"],
        "title": event["title"],
        "relevant": event["relevant"]
    }


async def retrieve_schedule(schedule):
    events = []
    events_collection = database.get_collection(schedule)
    async for event in events_collection.find():
        events.append(event_helper(event))
    return events

async def add_event(event: dict, schedule: str) -> dict:
    events_collection = database.get_collection(schedule)
    event = await events_collection.insert_one(event)
    new_event = await events_collection.find_one({"_id": event.inserted_id})
    return event_helper(new_event)