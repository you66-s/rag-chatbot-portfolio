from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    APP_NAME: str
    APP_VERSION: str

    FILE_ALLOWED_TYPES: str
    FILE_MAX_SIZE: int
    FILE_DEFAULT_CHUNK_SIZE: int

    GEMINI_MODEL_API_KEY: str
    GENERATION_MODEL_ID: str
    EMBEDDING_MODEL_ID: str
    EMBEDDING_OUTPUT_VECTOR_SIZE: int
    
    COLLECTION_NAME: str
    
    class Config:
        env_file = ".env"

def get_settings():
    return Settings()