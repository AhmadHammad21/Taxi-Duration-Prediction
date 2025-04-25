from dataclasses import dataclass
from dataclasses import dataclass, field
from typing import List
from datetime import datetime
from dateutil.relativedelta import relativedelta

@dataclass
class AppSettings:
    RAW_DATA_DIRECTORY: str = "data/raw"
    PROCESSED_DATA_DIRECTORY: str = "data/processed"

    DATA_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year_month}.parquet"

    TRAINING_DATA_DATE: dict = field(default_factory=lambda: {
        "start": "2024-01",
        "end": "2024-02" # Inclusive
    })

    TESTING_DATA_DATE: dict = field(default_factory=lambda: {
        "start": "2024-03",
        "end": "2024-03" # Inclusive
    })

    # # ================================ LLM Settings ================================
    # GENERATION_MODEL_ID: str = "gpt-4o-mini"
    # # GENERATION_MODEL_ID: str = "ALLaM-AI/ALLaM-7B-Instruct-preview"
    # EMBEDDING_MODEL_ID: str = "text-embedding-3-small"
    # # EMBEDDING_MODEL_ID: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    # EMBEDDING_MODEL_SIZE: int = 768

    # GENERATION_BACKEND: str = "OPENAI"
    # EMBEDDING_BACKEND: str = "OPENAI"

    # INPUT_DAFAULT_MAX_CHARACTERS: int = 1024
    # GENERATION_DAFAULT_MAX_TOKENS: int = 1024
    # GENERATION_DAFAULT_TEMPERATURE: float = 0.1
    # TOP_K: int = 10
    # TOP_P: float = 0.95

    # # ================================ Vector DB Settings ================================
    # # VECTOR_DB_BACKEND="QDRANT"
    # # VECTOR_DB_PATH="qdrant_db"
    # # VECTOR_DB_DISTANCE_METHOD="cosine"
    # VECTOR_STORE_PATH: str = "./store/faiss_index" # ../ because we go into src directory 
    # TOP_SIMILARITY_K: int = 3
    # CHUNK_SIZE: int = 1000
    # CHUNK_OVERLAP: int = 200


    # # ================================ Template Configs ================================
    # PRIMARY_LANG = "ar"
    # DEFAULT_LANG = "en"
    # # FILE_ALLOWED_TYPES=["text/plain", "application/pdf"]
    # # FILE_MAX_SIZE=10
    # # FILE_DEFAULT_CHUNK_SIZE=512000 # 512KB

    # # MONGODB_URL="mongodb://admin:admin@localhost:27007"
    # # MONGODB_DATABASE="mini-rag"



settings = AppSettings()