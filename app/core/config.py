import os

import dotenv

dotenv.load_dotenv()


OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
OPENWEATHERMAP_BASE_URL = os.getenv("OPENWEATHERMAP_BASE_URL")

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION_NAME = os.getenv("AWS_REGION_NAME", "eu-west-1")

S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
DYNAMODB_TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME")

LOGGING_DIR = "logs"
LOGGING_FILE_PATH = os.path.join(LOGGING_DIR, "app.log")

SETUP_SERVICES = os.getenv("SETUP_SERVICES", "False").strip().lower() in ("true", "1")

CACHE_MINUTES = 5
