from typing import Any

from sqlalchemy.orm import Session

from app.core.models import Employee, Log
from app.repositories.log_repository import LogRepository


class LogService:
    """Registra logs de auditoria na mesma transação da ação auditada."""

    def __init__(self, db: Session, actor: Employee | None = None):
        self.repository = LogRepository(db)
        self.actor = actor

    def register(
        self,
        action: str,
        table: str,
        record_id: int | None = None,
        data: dict[str, Any] | None = None,
    ) -> Log:
        # Não guarde CPF, CNPJ, e-mail ou senha em `data`: o log não tem máscara
        performed_by = f"employee:{self.actor.id}" if self.actor else "system"
        return self.repository.create(
            Log(action=action, table=table, record_id=record_id, data=data, performed_by=performed_by)
        )
