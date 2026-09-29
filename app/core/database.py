from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from .configs import URLS_CONFIG

database_url = URLS_CONFIG["DATABASE_URL"]

# check_same_thread só existe no driver do SQLite
connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}

engine = create_engine(database_url, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    """Dependência do FastAPI: abre uma sessão por requisição e fecha ao final."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
