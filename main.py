from pip import main
from fastapi import Depends, FastAPI
import google_calander_api

app = FastAPI()

@app.get("/test")
async def testapp():
    return {"i am running": True}

@app.post("/updateCalander")
async def update_calander():
    events = google_calander_api.get_cal_events()
    print(events)
    #todo: push to mongo with ofek