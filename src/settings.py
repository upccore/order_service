from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_connection_string: str
    catalog_base_url: str
    catalog_api_key: str
    payments_base_url: str
    payments_api_key: str
    callback_base_url: str

    @property
    def database_url(self) -> str:
        return self.postgres_connection_string.replace(
            "postgres://", "postgresql+asyncpg://", 1
        )

    class Config:
        env_file = ".env"


settings = Settings()
