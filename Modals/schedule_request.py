from pydantic import BaseModel

class ScheduleRequest(BaseModel):
    name: str
    relevant: str