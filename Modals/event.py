from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel

class Event(BaseModel):
    time: str
    title: str
    relevant: str