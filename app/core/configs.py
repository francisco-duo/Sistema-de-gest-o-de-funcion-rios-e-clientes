import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError(
        "A variável de ambiente DATABASE_URL não está definida. "
        "Crie um arquivo .env a partir do .env.example."
    )

URLS_CONFIG = {
    "DATABASE_URL": DATABASE_URL,
}
