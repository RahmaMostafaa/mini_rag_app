from fastapi import FastAPI 
from routes import base
from routes import data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings

app=FastAPI()

#Once system start
@app.on_event("startup")
async def startup_db_client():
    settings= get_settings()

#server
    app.mongo_conn = AsyncIOMotorClient(settings.MONGOBD_URL)
    #Specific Database in the server
    app.db_client = app.mongo_conn[settings.MONGOBD_DATABASE]

#close the database
@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongo_conn.close()

app.include_router(base.base_router)

app.include_router(data.data_router)
