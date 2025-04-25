from fastapi import FastAPI
from routes import base, taxi
# from motor.motor_asyncio import AsyncIOMotorClient
# from config.config import config
# from config.settings import settings
# from llms.llm_provider_factory import LLMProviderFactory
# from vector_dbs.providers.vector_store import VectorStore
# from llms.rag_provider import RAGProvider
# from llms.templates.template_parser import TemplateParser
# from mongo_db.chat_log_manager import ChatLogManager


async def lifespan(app: FastAPI):

    # MongoDb Connection
    # app.mongo_conn = AsyncIOMotorClient(config.MONGODB_URL)
    # app.db_client = app.mongo_conn[config.MONGODB_DATABASE]

    # app.chat_log_manager = ChatLogManager(
    #     mongo_conn=app.mongo_conn,
    #     db_client=app.db_client,
    #     collection_name=config.MONGODB_COLLECTION
    # )

    # app.template_parser = TemplateParser(
    #     language=settings.PRIMARY_LANG,
    #     default_language=settings.DEFAULT_LANG
    # )

    # llm_provider_factory = LLMProviderFactory(
    #     config=config,
    #     settings=settings
    # )

    # app.generation_client = llm_provider_factory.create(
    #     provider=settings.GENERATION_BACKEND
    # )
    # app.generation_client.set_generation_model(
    #     model_id=settings.GENERATION_MODEL_ID
    # )

    # app.embedding_client = llm_provider_factory.create(
    #     provider=settings.EMBEDDING_BACKEND
    # )
    # app.embedding_client.set_embedding_model(
    #     model_id=settings.EMBEDDING_MODEL_ID,
    #     embedding_size=settings.EMBEDDING_MODEL_SIZE
    # )

    # app.vector_store = VectorStore()
    # app.vector_store.load_vector_store(
    #     settings.VECTOR_STORE_PATH,
    #     app.embedding_client.embed_text
    # )

    # app.rag_client = RAGProvider(
    #     vectordb_client=app.vector_store,
    #     chat_log_manager=app.chat_log_manager,
    #     generation_client=app.generation_client,
    #     embedding_client=app.embedding_client,
    #     template_parser=app.template_parser
    # )
    
    yield  # This is where FastAPI runs the application

    # Closing connections
    # app.mongo_conn.close()

app = FastAPI(lifespan=lifespan)

app.include_router(base.base_router)
app.include_router(taxi.chatbot_router)