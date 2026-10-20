from fastapi import FastAPI 
from routes import base
from routes import data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from stores.llm.LLMProviderFactory import LLMProviderFactory
from stores.vectordb.VectoreDBProviderFactory import VectoreDBProviderFactory
app=FastAPI()

#Once system start
async def startup_spam():
    settings= get_settings()

#server
    app.mongo_conn = AsyncIOMotorClient(settings.MONGOBD_URL)
    #Specific Database in the server
    app.db_client = app.mongo_conn[settings.MONGOBD_DATABASE]

    llm_provider_factory = LLMProviderFactory(Settings)
    vectordb_provider_factory = VectoreDBProviderFactory(Settings)

    #generation client 
    #create genereation model object(OpenAI)
    app.generation_client = llm_provider_factory.create(provider=settings.GENERATION_BACKEND)
    #from (OpenAI) object use function of set_generation_model to get specific model in OpenAI
    app.generation_client.set_generation_model(model_id =settings.GENERATION_MODEL_ID)

    #embedding client 
    #create genereation model object(CoHere)
    app.embedding_client = llm_provider_factory.create(provider=settings.EMBEDDING_BACKEND)
    #from (CoHere) object use function of set_generation_model to get specific model in CoHere
    app.embedding_client.set_embedding_model(model_id=settings.EMBEDDING_MODEL_ID
                                             embedding_size=settings.EMBEDDING_MODEL_SIZE)

    # vector db client
    app.vectordb_client = vectordb_provider_factory.create(provider = settings.VECTOR_DB_BACKEND)
   
   
    app.vectordb_client.connect()
#close the database
async def shutdown__spam():
    app.mongo_conn.close()
    app.vectordb_client.disconnect()


app.router.lifespam.on_startup.append(startup_spam)
app.router.lifespam.on_shutdown.append(shutdown__spam)

app.include_router(base.base_router)

app.include_router(data.data_router)
