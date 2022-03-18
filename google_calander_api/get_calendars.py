from pydantic import Json
from .cal_setup import get_calendar_service
from configparser import ConfigParser

# Read config.ini file
config_obj = ConfigParser()
config_obj.read("./google_calander_api/config.ini")
print(config_obj.sections())

calanderid = config_obj["googleCalander"]["calendarId"]


def get_cal_list():
    """get list of all user's calanders

    Returns:
        list: list of calanders metadata.
    """
    service = get_calendar_service()
    calendars_result = service.calendarList().list().execute()
    calendars = calendars_result.get('items', [])
    return calendars


def get_cal_events():
    """return list of all calander's events.

    Returns:
        list: all calander events as jsons.
    """
    service = get_calendar_service()
    events = service.events().list(calendarId=calanderid).execute()
    return events["items"]