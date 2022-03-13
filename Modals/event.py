from pydantic import BaseModel

class Event(BaseModel):
    kind: str
    etag: str
    id: str
    status: str
    htmlLink: str
    created: str
    updated: str
    summary: str
    creator: any
    organizer: any
    start: any
    end: any
    iCalUID: str
    sequence: int
    reminders: any
    eventType: str