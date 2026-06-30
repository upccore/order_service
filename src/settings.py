from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    catalog_base_url: str
    catalog_api_key: str

    class Config:
        env_file = ".env"


settings = Settings()
