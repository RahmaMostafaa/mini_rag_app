from fastapi import FastAPI 
from routes import base
from routes import data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from stores.llm.LLMProviderFactory import LLMProviderFactory
app=FastAPI()

#Once system start
@app.on_event("startup")
async def startup_db_client():
    settings= get_settings()

#server
    app.mongo_conn = AsyncIOMotorClient(settings.MONGOBD_URL)
    #Specific Database in the server
    app.db_client = app.mongo_conn[settings.MONGOBD_DATABASE]

    llm_provider_factory = LLMProviderFactory(Settings)

    #generation client 
    app.generation_client = llm_provider_factory.create(provider=settings.GENERATION_BACKEND)
    app.generation_client.set_generation_model(model_id =settings.GENERATION_MODEL_ID)
    #embedding client 
    app.embedding_client = llm_provider_factory.create(provider=settings.EMBEDDING_BACKEND)
    app.embedding_client.set_embedding_model(model_id=settings.EMBEDDING_MODEL_ID
                                             embedding_size=settings.EMBEDDING_MODEL_SIZE)

#close the database
@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongo_conn.close()

app.include_router(base.base_router)

app.include_router(data.data_router)
