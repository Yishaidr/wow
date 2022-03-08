from fastapi import Depends, FastAPI, Body
import DAL.database as db
from fastapi.encoders import jsonable_encoder
from Modals.schedule_request import ScheduleRequest

app = FastAPI()

@app.get("/test")
async def testapp():
    return {"i am running": True}

@app.post("/sendScheduled")
async def sendschedule(schedule_request: ScheduleRequest):
    schedule = jsonable_encoder(schedule_request)
    events = await db.retrieve_schedule(schedule["name"])
    relevant_events = []
    for event in events:
        if event["relevant"] == schedule["relevant"] or event["relevant"] == "all":
            relevant_events.append(event)
    return relevant_events