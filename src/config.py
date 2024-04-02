# from dotenv import load_dotenv
# import os

# load_dotenv()

# DB_HOST = os.environ.get("DB_HOST")
# DB_PORT = os.environ.get("DB_PORT")
# DB_NAME = os.environ.get("DB_NAME")
# DB_USER = os.environ.get("DB_USER")
# DB_PASS = os.environ.get("DB_PASS")

# SECRET_KEY_JWT = os.environ.get("SECRET_KEY_JWT")
# ALGORITHM = os.environ.get("ALGORITHM")

# BOT_TOKEN = os.environ.get("BOT_TOKEN")
# WEBHOOK_HOST = os.environ.get("WEBHOOK_HOST")
# WEBHOOK_PATH = os.environ.get("WEBHOOK_PATH")


# BUCKET_NAME = os.environ.get("BUCKET_NAME")
# ENDPOINT_URL = os.environ.get("ENDPOINT_URL")
# AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
# AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")


from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PYTHONPATH: str

    # REDIS_HOST: str
    # REDIS_PORT: int

    SECRET_KEY_JWT: str
    ALGORITHM: str

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    MODE: str

    BOT_TOKEN: str

    WEBHOOK_HOST: str
    WEBHOOK_PATH: str

    BUCKET_NAME: str
    ENDPOINT_URL: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str

    API_ID: str
    API_KEY: str

    @property
    def DB_URL(self):
        return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")

    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8')


settings = Settings()
