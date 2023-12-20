from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

SECRET_KEY_JWT = os.environ.get("SECRET_KEY_JWT")
ALGORITHM = os.environ.get("ALGORITHM")

BOT_TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_HOST = os.environ.get("WEBHOOK_HOST")
WEBHOOK_PATH = os.environ.get("WEBHOOK_PATH")


BUCKET_NAME = os.environ.get("BUCKET_NAME")
ENDPOINT_URL = os.environ.get("ENDPOINT_URL")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
