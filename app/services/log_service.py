from typing import Any

from sqlalchemy.orm import Session

from app.core.models import Log
from app.repositories.log_repository import LogRepository


class LogService:
    """Registra logs de auditoria na mesma transação da ação auditada."""

    def __init__(self, db: Session):
        self.repository = LogRepository(db)

    def register(
        self,
        action: str,
        table: str,
        record_id: int | None = None,
        data: dict[str, Any] | None = None,
        performed_by: str | None = None,  # TODO: preencher com o usuário autenticado quando houver login
    ) -> Log:
        # Não guarde CPF, CNPJ ou e-mail em `data`: o log não tem máscara
        return self.repository.create(
            Log(action=action, table=table, record_id=record_id, data=data, performed_by=performed_by)
        )
