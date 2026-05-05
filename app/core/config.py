from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    # APP METADATA
    APP_NAME: str
    APP_VERSION: str

    # FILE PROCESSING
    FILE_ALLOWED_TYPES: str
    FILE_MAX_SIZE: int
    FILE_DEFAULT_CHUNK_SIZE: int

    # LLM
    GEMINI_MODEL_API_KEY: str
    GENERATION_MODEL_ID: str
    EMBEDDING_MODEL_ID: str
    EMBEDDING_OUTPUT_VECTOR_SIZE: int
    
    # DATABASE
    COLLECTION_NAME: str
    DB_DATABASE_NAME: str
    DB_HOSTNAME: str
    DB_USER_NAME: str
    DB_PASSWORD: str
    DB_PORT: str
    
    class Config:
        env_file = ".env"

def get_settings():
    return Settings()