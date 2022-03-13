import json
from fastapi import Depends, FastAPI, Body
import DAL.database as db
from fastapi.encoders import jsonable_encoder
from Modals.schedule_request import ScheduleRequest
from pip import main
import google_calander_api
from fastapi.middleware.cors import CORSMiddleware
from configparser import ConfigParser

# Read config.ini file
config_obj = ConfigParser()
config_obj.read("mainconfig.ini")

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.post("/updateCalander", description="Get Current calander from google and push to mongo")
async def update_calander():
    events = google_calander_api.get_cal_events()
    print(events)
    # todo: push to mongo with ofek


@app.get("/getListOfPeople/pluga", description="Get all pluga's optional names")
async def get_pluga_list():
    pluga_names = config_obj["pluga"]["names"]
    pluga_names_json = json.loads(pluga_names)
    array = []
    for name in pluga_names_json:
        array.append({"label": name, "value": name})
    return array


@app.get("/getcalander/{pluga_name}", description="Get spesific pluga's schedule")
async def get_pluga_calander(pluga_name: str):
    # temp!!!
    # pulles all events directly from google (not mongo)
    events = google_calander_api.get_cal_events()
    return(events)
    # todo: get spesific plugas schedual
