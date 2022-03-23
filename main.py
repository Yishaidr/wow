import datetime
import imp
import json
from re import A
from urllib import response
from fastapi import Depends, FastAPI, Body, HTTPException
import DAL.database as db
from fastapi.encoders import jsonable_encoder
from Modals.schedule_request import ScheduleRequest
from pip import main
import google_calander_api
from fastapi.middleware.cors import CORSMiddleware
from configparser import ConfigParser
from routers import listofpeoplerouter as listofpeoplerouter
# Read config.ini file
config_obj = ConfigParser()
config_obj.read("mainconfig.ini")

app = FastAPI()

app.include_router(listofpeoplerouter)

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
    events = await db.retrieve_schedule(schedule["date"])
    relevant_events = []
    for event in events:
        if event["relevant"] == schedule["relevant"] or event["relevant"] == "all":
            relevant_events.append(event)
    return relevant_events


def get_group_from_description(description: str = None):
    """splits description field from google calander and returnes its group.
        The group will be in the first line of the description.

    Args:
        description (str, optional): description from google calander. Defaults to None.

    Returns:
        _type_: _description_
    """
    # Some of the messages can come with html headers as string (copy paste shit).
    if description.startswith('<html-blob>'):
        description = description[11:]
    description = description.replace('<', "\n")
    first_line_of_description = description.split('\n', 1)[0]
    return first_line_of_description


def set_event_group(events):
    for event in events:
        if "description" in event:
            event["group"] = get_group_from_description(event["description"])
            event["description"] = event["description"].split('\n', 1)[0]
        else:
            event["group"] = "Unknown"
    return events


@app.post("/updateCalander", description="Get Current calander from google and push to mongo")
async def update_calander():
    events = google_calander_api.get_cal_events()
    events_with_group = set_event_group(events)
    response = await db.add_events(events_with_group, events_with_group[0]["start"]["dateTime"][:10])
    return response


def minimize_event(event) -> json:
    newjson = {}
    newjson["start"] = event["start"]["dateTime"][11:19]
    newjson["end"] = event["end"]["dateTime"][11:19]
    newjson["summery"] = event["summary"]
    try:
        newjson["description"] = event["description"]
    except:
        print("description doesn't exist")
    return newjson


def get_team_tree(group_name: str) -> list:
    """function gets group name and retuen array of its hirarchy.

    Args:
        group_name (str): group hirarcy name - example: amram or digitl.

    Returns:
        list : list of strings of hirarcy. example: amram -> [amram, hatam, hermon].
    """
    pluga_names = config_obj["pluga"]["names"]
    pluga_names_json = json.loads(pluga_names)
    tree_list = []
    for pluga in pluga_names_json:
        if group_name == pluga:
            tree_list.append(pluga)
            break
        for maarach in pluga_names_json[pluga]:
            if group_name == maarach:
                tree_list.append(pluga)
                tree_list.append(maarach)
                break
            for team in pluga_names_json[pluga][maarach]:
                if group_name == team:
                    tree_list.append(team)
                    tree_list.append(maarach)
                    tree_list.append(pluga)
                    break
        if not tree_list:
            return None
    return tree_list


@app.get("/getcalander/{team_name}/{date}", description="Get spesific teams's schedule for given date. example: 2022-03-12")
async def get_pluga_calander(team_name: str, date:str):
    """function gets group name (pluga, maarach, team) and return it's given schedual

    Args:
        team_name (str): team name - example: amram or digital.
    """
    events_with_group = await db.retrieve_schedule(date)
    team_tree = get_team_tree(team_name)
    if team_tree is None:
        raise HTTPException(
            status_code=404, detail="Item not found""Team name doesn't exist")
    tomorrow_events = []
    for event in events_with_group:
        if event["group"] in team_tree:
            tomorrow_events.append(minimize_event(event))
    return(tomorrow_events)


@app.get("/getcalandertomorrow/{team_name}", description="Get spesific teams's schedule for tomorrow")
async def get_tomorrow_pluga_calander(team_name: str):
    """function gets group name (pluga, maarach, team) and return it's given schedual

    Args:
        team_name (str): team name - example: amram or digital.
    """
    date = str(datetime.date.today() + datetime.timedelta(days=1))[0:10]
    events_with_group = await db.retrieve_schedule(date)
    team_tree = get_team_tree(team_name)
    if team_tree is None:
        raise HTTPException(
            status_code=404, detail="Item not found""Team name doesn't exist")
    tomorrow_events = []
    for event in events_with_group:
        if event["group"] in team_tree:
            tomorrow_events.append(minimize_event(event))
    return(tomorrow_events)


@app.post("/test/getCalander", description="Get Current calander from google")
async def update_calander():
    events = google_calander_api.get_cal_events()
    return events
