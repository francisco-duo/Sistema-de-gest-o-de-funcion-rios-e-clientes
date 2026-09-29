from sqlalchemy.orm import Session

from app.core.models import Log


class LogRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, log: Log) -> Log:
        self.db.add(log)
        self.db.flush()
        return log
