from pydantic import BaseModel

class Event(BaseModel):
    time: str
    title: str
    relevant: str