from pydantic import BaseModel

class ScheduleRequest(BaseModel):
    date: str
    relevant: str