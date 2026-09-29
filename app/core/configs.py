import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError(
        "A variável de ambiente DATABASE_URL não está definida. Crie um arquivo .env a partir do .env.example."
    )

URLS_CONFIG = {
    "DATABASE_URL": DATABASE_URL,
}

# A SECRET_KEY é validada em app/core/security.py, para as migrations do
# Alembic (que importam este módulo) não precisarem dela.
SECURITY_CONFIG = {
    "SECRET_KEY": os.getenv("SECRET_KEY"),
    "ALGORITHM": "HS256",
    "ACCESS_TOKEN_EXPIRE_MINUTES": int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")),
}
