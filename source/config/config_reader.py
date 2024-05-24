from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

OWNER_ID = 435918797
ADMINS_LIST = (435918797,)

BANNED_USERS = ()


class EnvBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


class DBSettings(EnvBaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: SecretStr
    DB_NAME: str

    @property
    def DATABASE_URL_asyncpg(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS.get_secret_value()}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class Settings(DBSettings):
    DEBUG: bool = False


settings = Settings()
