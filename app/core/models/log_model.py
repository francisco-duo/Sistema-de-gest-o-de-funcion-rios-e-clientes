from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String, nullable=False)                     # Ex: "CREATE_USER", "DELETE_CLIENT"
    table = Column(String, nullable=False)                      # Ex: "users", "clients"
    record_id = Column(Integer, nullable=True)                  # ID do registro afetado
    performed_by = Column(String, nullable=True)                # Nome ou ID de quem executou
    timestamp = Column(DateTime, default=datetime.now())       # Data/hora da ação
    data = Column(JSON, nullable=True)

    def __repr__(self):
        return f"<Log(id={self.id}, action={self.action}, table={self.table}, record_id={self.record_id}, performed_by={self.performed_by}, timestamp={self.timestamp})>"