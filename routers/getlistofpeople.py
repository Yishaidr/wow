import json
from fastapi import APIRouter
from configparser import ConfigParser

router = APIRouter()

config_obj = ConfigParser()
config_obj.read("mainconfig.ini")

@router.get("/getListOfPeople/pluga", description="Get all pluga's optional names")
async def get_pluga_list():
    pluga_names = config_obj["pluga"]["names"]
    pluga_names_json = json.loads(pluga_names)
    pluga_names_list = []
    for name in pluga_names_json:
        pluga_names_list.routerend({"label": name, "value": name})
    return pluga_names_list


@router.get("/getListOfPeople/{pluga_name}/maarach", description="Get all maarach names in a pluga")
async def get_maarach_list_in_pluga(pluga_name: str) -> list:
    pluga_names = config_obj["pluga"]["names"]
    pluga_names_json = json.loads(pluga_names)
    return list(pluga_names_json[pluga_name].keys())


@router.get("/getListOfPeople/{pluga_name}/{maarach}/team", description="Get all team names in a maarach")
async def get_team_list_in_maarach(pluga_name: str, maarach: str) -> list:
    pluga_names = config_obj["pluga"]["names"]
    pluga_names_json = json.loads(pluga_names)
    return pluga_names_json[pluga_name][maarach]


@router.get("/getListOfPeople/team", description="Get all team names")
async def get_team_list() -> list:
    pluga_names = config_obj["pluga"]["names"]
    pluga_names_json = json.loads(pluga_names)
    team_list = []
    for pluga in pluga_names_json:
        for maarach in pluga_names_json[pluga]:
            for team in pluga_names_json[pluga][maarach]:
                team_list.routerend(team)
    return team_list


@router.get("/getListOfPeople/all", description="Get all pluga, maarach and team names")
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
