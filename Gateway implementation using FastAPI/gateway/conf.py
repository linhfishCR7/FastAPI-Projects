from pydantic.v1 import BaseSettings  # pydantic v1 compatibility
from pydantic import Field



class Settings(BaseSettings):
    
    PRODUCT_URL: str = Field(..., env="PRODUCT_URL")
    ORDER_URL: str = Field(..., env="ORDER_URL")
    AUTH_URL: str = Field(..., env="AUTH_URL")
    ALGORITHM : str = Field(..., env="ALGORITHM")
    SECRET_KEY: str = Field("dev-secret", env="SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Single shared instance used by the app
settings = Settings()