import motor.motor_asyncio
from bson.objectid import ObjectId
from pymongo import InsertOne


MONGO_DETAILS = "mongodb://admin:wowisofek@wowmongo.eastus.azurecontainer.io:27017"

wow= motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = wow.schedule


def event_helper(event) -> dict:
    return {
        "kind": event["kind"],
        "etag": event["etag"],
        "id": event["id"],
        "status": event["status"],
        "htmlLink": event["htmlLink"],
        "created": event["created"],
        "updated": event["updated"],
        "group": event["group"],
        "summary": event["summary"],
        "creator": event["creator"],
        "organizer": event["organizer"],
        "start": event["start"],
        "end": event["end"],
        "iCalUID": event["iCalUID"],
        "sequence": event["sequesnce"],
        "reminders": event["reminders"],
        "eventType": event["eventType"]
    }


async def retrieve_schedule(schedule):
    events = []
    events_collection = database.get_collection(schedule)
    async for event in events_collection.find():
        events.append(event_helper(event))
    return events

async def add_event(event: dict, schedule: str) -> dict:
    events_collection = await get_or_create_collection(schedule) 
    event = await events_collection.insert_one(event)
    new_event = await events_collection.find_one({"_id": event.inserted_id})
    return event_helper(new_event)

async def add_events(events: dict, schedule: str):
    events_collection = await get_or_create_collection(schedule)
    requests = [InsertOne(e) for e in events] 
    events_request = await events_collection.bulk_write(requests)
    if events_request.inserted_count == len(events):
        return "Succesed"
    return "Faild"

async def get_or_create_collection(collection: str):
    collection_names = await database.list_collection_names()
    if collection not in collection_names:
        await database.create_collection(collection)  
    return database.get_collection(collection)