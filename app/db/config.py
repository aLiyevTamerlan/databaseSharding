from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_SHARDS: str


    model_config = SettingsConfigDict(env_file=".env")
    @property
    def get_shards(self):
        return self.DB_SHARDS.split(",")

settings = Settings()


