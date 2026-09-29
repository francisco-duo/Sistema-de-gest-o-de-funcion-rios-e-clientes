from sqlalchemy.orm import Session

from app.core.models import Client, Employee, EmployeeLevel
from app.repositories.category_repository import CategoryRepository
from app.repositories.employee_repository import EmployeeRepository
from app.schemas.employee_schema import EmployeeCreate
from app.services.client_service import ClientService
from app.services.exceptions import BusinessRuleError, ConflictError, NotFoundError
from app.services.log_service import LogService

# Quantidade máxima de clientes que um funcionário JUNIOR pode atender
MAX_CLIENTS_JUNIOR = 5


class EmployeeService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = EmployeeRepository(db)
        self.categories = CategoryRepository(db)
        self.clients = ClientService(db)
        self.logs = LogService(db)

    def create(self, data: EmployeeCreate) -> Employee:
        if self.repository.get_by_email(data.email):
            raise ConflictError("Já existe um funcionário com este e-mail.")
        if self.repository.get_by_cpf(data.cpf):
            raise ConflictError("Já existe um funcionário com este CPF.")
        if data.category_id is not None and self.categories.get_by_id(data.category_id) is None:
            raise NotFoundError("Categoria não encontrada.")

        employee = self.repository.create(Employee(**data.model_dump()))
        self.logs.register(
            "CREATE_EMPLOYEE", Employee.__tablename__, employee.id,
            {"name": employee.name, "level": employee.level.value},
        )

        self.db.commit()
        self.db.refresh(employee)
        return employee

    def get(self, employee_id: int) -> Employee:
        employee = self.repository.get_by_id(employee_id)
        if employee is None:
            raise NotFoundError("Funcionário não encontrado.")
        return employee

    def list_paginated(
        self, *, name: str | None, level: EmployeeLevel | None, category_id: int | None, skip: int, limit: int,
    ) -> tuple[list[Employee], int]:
        return self.repository.list_paginated(name=name, level=level, category_id=category_id, skip=skip, limit=limit)

    def list_clients(self, employee_id: int) -> list[Client]:
        return list(self.get(employee_id).clients)

    def link_client(self, employee_id: int, client_id: int) -> Client:
        employee = self.get(employee_id)
        client = self.clients.get(client_id)

        if client in employee.clients:
            raise ConflictError("Este cliente já está vinculado ao funcionário.")
        if employee.level == EmployeeLevel.JUNIOR and len(employee.clients) >= MAX_CLIENTS_JUNIOR:
            raise BusinessRuleError(
                f"Funcionários JUNIOR podem atender no máximo {MAX_CLIENTS_JUNIOR} clientes."
            )

        employee.clients.append(client)
        self.logs.register(
            "LINK_CLIENT", Employee.__tablename__, employee.id, {"client_id": client.id},
        )

        self.db.commit()
        return client

    def unlink_client(self, employee_id: int, client_id: int) -> None:
        employee = self.get(employee_id)
        client = self.clients.get(client_id)

        if client not in employee.clients:
            raise NotFoundError("Este cliente não está vinculado ao funcionário.")

        employee.clients.remove(client)
        self.logs.register(
            "UNLINK_CLIENT", Employee.__tablename__, employee.id, {"client_id": client.id},
        )

        self.db.commit()
