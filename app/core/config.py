from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PINECONE_API_KEY: str
    PINECONE_ENV: str = "us-east-1"
    PINECONE_INDEX_NAME: str = "beebots"
    GROQ_API_KEY: str
    REDIS_URL: str = "redis://localhost:6379/0"
    HF_API_KEY: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
