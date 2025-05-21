import os

from dotenv import load_dotenv

load_dotenv()

URLS_CONFIG = {
    "DATABASE_URL": str(os.getenv("DATABASE_URL")),
}
