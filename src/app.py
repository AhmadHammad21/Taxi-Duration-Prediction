from fastapi import FastAPI
from .routes import base, taxi
# from motor.motor_asyncio import AsyncIOMotorClient
# from config.config import config
# from config.settings import settings
# from llms.llm_provider_factory import LLMProviderFactory
# from vector_dbs.providers.vector_store import VectorStore
# from llms.rag_provider import RAGProvider
# from llms.templates.template_parser import TemplateParser
# from mongo_db.chat_log_manager import ChatLogManager


async def lifespan(app: FastAPI):
    
    yield  # This is where FastAPI runs the application


app = FastAPI(lifespan=lifespan)

app.include_router(base.base_router)
app.include_router(taxi.taxi_router)