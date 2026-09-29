from datetime import datetime
from typing import Any

from sqlalchemy import JSON, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Log(Base):
    __tablename__ = 'logs'

    id: Mapped[int] = mapped_column(primary_key=True)
    action: Mapped[str] = mapped_column(String(50))                     # Ex: "CREATE_EMPLOYEE", "DELETE_CLIENT"
    table: Mapped[str] = mapped_column(String(50))                      # Ex: "employees", "clients"
    record_id: Mapped[int | None]                                       # ID do registro afetado
    performed_by: Mapped[str | None] = mapped_column(String(100))       # Nome ou ID de quem executou
    timestamp: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())  # Data/hora da ação (preenchida pelo banco)
    data: Mapped[dict[str, Any] | None] = mapped_column(JSON)

    def __repr__(self):
        return f"<Log(id={self.id}, action={self.action}, table={self.table}, record_id={self.record_id}, performed_by={self.performed_by}, timestamp={self.timestamp})>"
