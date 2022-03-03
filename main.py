from fastapi import Depends, FastAPI


app = FastAPI()

@app.get("/test")
async def testapp():
    return {"i am running": True}


