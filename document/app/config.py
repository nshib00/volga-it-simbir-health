from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings

load_dotenv(find_dotenv(filename='document/.document.env'))


class DocumentSettings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    ELASTIC_URL: str
    ELASTIC_USER: str
    ELASTIC_PASSWORD: str

    BASE_AUTH_URL: str
    BASE_ACCOUNTS_URL: str
    BASE_DOCTORS_URL: str
    BASE_HOSPITAL_URL: str
    
    @property
    def DB_URL(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
    
    
settings = DocumentSettings()
    
