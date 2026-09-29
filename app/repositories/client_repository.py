from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.models import Client


class ClientRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, client: Client) -> Client:
        self.db.add(client)
        self.db.flush()  # gera o id sem fazer commit; o commit fica com o service
        return client

    def get_by_id(self, client_id: int) -> Client | None:
        return self.db.get(Client, client_id)

    def get_by_email(self, email: str) -> Client | None:
        return self.db.scalar(select(Client).where(Client.email == email))

    def get_by_cnpj(self, cnpj: str) -> Client | None:
        return self.db.scalar(select(Client).where(Client.cnpj == cnpj))

    def list_paginated(self, *, name: str | None = None, skip: int = 0, limit: int = 20) -> tuple[list[Client], int]:
        query = select(Client)
        if name:
            query = query.where(Client.name.ilike(f"%{name}%"))

        total = self.db.scalar(select(func.count()).select_from(query.subquery()))
        items = self.db.scalars(query.order_by(Client.id).offset(skip).limit(limit)).all()
        return list(items), total
