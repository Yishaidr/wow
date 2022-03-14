import json
from re import A
from urllib import response
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


def get_group_from_description(description=None):
    print(description)
    return description


def set_event_group(events):
    for i in events:
        if "description" in i:
            i["group"] = get_group_from_description(i["description"])
            i["group"] = "a"
        else:
            i["group"] = "Unknown"
    return events


@app.post("/updateCalander", description="Get Current calander from google and push to mongo")
async def update_calander():
    events = google_calander_api.get_cal_events()
    events_with_group = set_event_group(events)
    response = await db.add_events(events_with_group, events_with_group[0]["start"]["dateTime"][:10])
    return response


@app.get("/getListOfPeople/pluga", description="Get all pluga's optional names")
async def get_pluga_list():
    pluga_names = config_obj["pluga"]["names"]
    pluga_names_json = json.loads(pluga_names)
    array = []
    for name in pluga_names_json:
        array.append({"label": name, "value": name})
    return array


@app.get("/getListOfPeople/{pluga_name}/maarach", description="Get all maarach names in a pluga")
async def get_maarach_list_in_pluga(pluga_name: str) -> list:
    pluga_names = config_obj["pluga"]["names"]
    pluga_names_json = json.loads(pluga_names)
    return list(pluga_names_json[pluga_name].keys())


@app.get("/getListOfPeople/{pluga_name}/{maarach}/team", description="Get all team names in a maarach")
async def get_team_list_in_maarach(pluga_name: str, maarach: str) -> list:
    pluga_names = config_obj["pluga"]["names"]
    pluga_names_json = json.loads(pluga_names)
    return pluga_names_json[pluga_name][maarach]


@app.get("/getListOfPeople/team", description="Get all team names")
async def get_team_list() -> list:
    pluga_names = config_obj["pluga"]["names"]
    pluga_names_json = json.loads(pluga_names)
    team_list = []
    for pluga in pluga_names_json:
        for maarach in pluga_names_json[pluga]:
            for team in pluga_names_json[pluga][maarach]:
                team_list.append(team)
    return team_list


@app.get("/getListOfPeople/all", description="Get all pluga, maarach and team names")
async def get_name_list() -> list:
    pluga_names = config_obj["pluga"]["names"]
    pluga_names_json = json.loads(pluga_names)
    names_list = set()
    for pluga in pluga_names_json:
        names_list.add(pluga)
        for maarach in pluga_names_json[pluga]:
            names_list.add(maarach)
            for team in pluga_names_json[pluga][maarach]:
                names_list.add(team)
    return names_list


@app.get("/getcalander/{pluga_name}", description="Get spesific pluga's schedule")
async def get_pluga_calander(pluga_name: str):
    # temp!!!
    # pulles all events directly from google (not mongo)
    events = google_calander_api.get_cal_events()
    return(events)
    # todo: get spesific plugas schedual


@app.post("/test/getCalander", description="Get Current calander from google")
async def update_calander():
    events = google_calander_api.get_cal_events()
    return events
