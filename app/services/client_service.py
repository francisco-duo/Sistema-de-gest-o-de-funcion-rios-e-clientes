from sqlalchemy.orm import Session

from app.core.models import Client, Employee
from app.repositories.client_repository import ClientRepository
from app.schemas.client_schema import ClientCreate
from app.services.exceptions import ConflictError, NotFoundError
from app.services.log_service import LogService


class ClientService:
    def __init__(self, db: Session, actor: Employee | None = None):
        self.db = db
        self.repository = ClientRepository(db)
        self.logs = LogService(db, actor)

    def create(self, data: ClientCreate) -> Client:
        if self.repository.get_by_email(data.email):
            raise ConflictError("Já existe um cliente com este e-mail.")
        if self.repository.get_by_cnpj(data.cnpj):
            raise ConflictError("Já existe um cliente com este CNPJ.")

        client = self.repository.create(Client(**data.model_dump()))
        self.logs.register("CREATE_CLIENT", Client.__tablename__, client.id, {"name": client.name})

        self.db.commit()
        self.db.refresh(client)
        return client

    def get(self, client_id: int) -> Client:
        client = self.repository.get_by_id(client_id)
        if client is None:
            raise NotFoundError("Cliente não encontrado.")
        return client

    def list_paginated(self, *, name: str | None, skip: int, limit: int) -> tuple[list[Client], int]:
        return self.repository.list_paginated(name=name, skip=skip, limit=limit)
