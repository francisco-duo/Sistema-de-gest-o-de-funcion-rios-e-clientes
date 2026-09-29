from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.models import EmployeeLevel
from app.schemas.client_schema import ClientRead
from app.schemas.employee_schema import EmployeeClientLink, EmployeeCreate, EmployeeRead
from app.schemas.pagination import Page
from app.services.employee_service import EmployeeService

router = APIRouter(prefix="/employees", tags=["Funcionários"])


def get_employee_service(db: Session = Depends(get_db)) -> EmployeeService:
    return EmployeeService(db)


EmployeeServiceDep = Annotated[EmployeeService, Depends(get_employee_service)]


@router.post("", response_model=EmployeeRead, status_code=status.HTTP_201_CREATED)
def create_employee(data: EmployeeCreate, service: EmployeeServiceDep):
    return service.create(data)


@router.get("", response_model=Page[EmployeeRead])
def list_employees(
    service: EmployeeServiceDep,
    name: Annotated[str | None, Query(description="Filtra pelo nome (contém)")] = None,
    level: EmployeeLevel | None = None,
    category_id: int | None = None,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
):
    items, total = service.list_paginated(name=name, level=level, category_id=category_id, skip=skip, limit=limit)
    return Page(items=items, total=total, skip=skip, limit=limit)


@router.get("/{employee_id}", response_model=EmployeeRead)
def get_employee(employee_id: int, service: EmployeeServiceDep):
    return service.get(employee_id)


@router.get("/{employee_id}/clients", response_model=list[ClientRead])
def list_employee_clients(employee_id: int, service: EmployeeServiceDep):
    return service.list_clients(employee_id)


@router.post("/{employee_id}/clients", response_model=ClientRead, status_code=status.HTTP_201_CREATED)
def link_client(employee_id: int, data: EmployeeClientLink, service: EmployeeServiceDep):
    return service.link_client(employee_id, data.client_id)


@router.delete("/{employee_id}/clients/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def unlink_client(employee_id: int, client_id: int, service: EmployeeServiceDep):
    service.unlink_client(employee_id, client_id)
