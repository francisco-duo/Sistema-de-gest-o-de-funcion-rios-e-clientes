from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.models import Employee, EmployeeLevel


class EmployeeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, employee: Employee) -> Employee:
        self.db.add(employee)
        self.db.flush()  # gera o id sem fazer commit; o commit fica com o service
        return employee

    def get_by_id(self, employee_id: int) -> Employee | None:
        return self.db.get(Employee, employee_id)

    def get_by_email(self, email: str) -> Employee | None:
        return self.db.scalar(select(Employee).where(Employee.email == email))

    def get_by_cpf(self, cpf: str) -> Employee | None:
        return self.db.scalar(select(Employee).where(Employee.cpf == cpf))

    def list_paginated(
        self,
        *,
        name: str | None = None,
        level: EmployeeLevel | None = None,
        category_id: int | None = None,
        skip: int = 0,
        limit: int = 20,
    ) -> tuple[list[Employee], int]:
        query = select(Employee)
        if name:
            query = query.where(Employee.name.ilike(f"%{name}%"))
        if level:
            query = query.where(Employee.level == level)
        if category_id is not None:
            query = query.where(Employee.category_id == category_id)

        total = self.db.scalar(select(func.count()).select_from(query.subquery()))
        items = self.db.scalars(query.order_by(Employee.id).offset(skip).limit(limit)).all()
        return list(items), total
