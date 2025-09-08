from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str = "mongodb://127.0.0.1:27017"
    MONGO_DB_NAME: str = "invoice"
    JWT_SECRET_KEY: str = "your_super_secret_key"
    JWT_ALGORITHM: str = "HS256"
    
    class Config:
        env_file = ".env"

settings = Settings()