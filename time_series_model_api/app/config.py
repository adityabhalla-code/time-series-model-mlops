import sys
from typing import List
from pydantic import AnyHttpUrl , BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/app/v1"

    BACKEND_CORS_ORIGIN:List[AnyHttpUrl]=[
        "http://localhost:3000",
        "http://localhost:8000",
        "https://localhost:3000",
        "https://localhost:8000"
    ]

    PROJECT_NAME : str = "Prophet Model prediction API "

    class Config:
        case_sensitive = True

settings = Settings()