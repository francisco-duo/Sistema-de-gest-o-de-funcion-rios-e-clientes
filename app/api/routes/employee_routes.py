from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies import WRITE_LEVELS, CurrentEmployee, DbSession, can_view_sensitive, require_levels
from app.core.models import EmployeeLevel
from app.schemas.client_schema import ClientRead
from app.schemas.employee_schema import EmployeeClientLink, EmployeeCreate, EmployeeRead
from app.schemas.pagination import Page
from app.services.employee_service import EmployeeService

router = APIRouter(prefix="/employees", tags=["Funcionários"])


def get_employee_service(db: DbSession, current: CurrentEmployee) -> EmployeeService:
    return EmployeeService(db, actor=current)


EmployeeServiceDep = Annotated[EmployeeService, Depends(get_employee_service)]


@router.post(
    "",
    response_model=EmployeeRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_levels(EmployeeLevel.ADMIN))],
)
def create_employee(data: EmployeeCreate, service: EmployeeServiceDep, current: CurrentEmployee):
    employee = service.create(data)
    return EmployeeRead.from_model(employee, show_sensitive=can_view_sensitive(current))


@router.get("", response_model=Page[EmployeeRead])
def list_employees(
    service: EmployeeServiceDep,
    current: CurrentEmployee,
    name: Annotated[str | None, Query(description="Filtra pelo nome (contém)")] = None,
    level: EmployeeLevel | None = None,
    category_id: int | None = None,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
):
    items, total = service.list_paginated(name=name, level=level, category_id=category_id, skip=skip, limit=limit)
    show = can_view_sensitive(current)
    return Page(
        items=[EmployeeRead.from_model(e, show_sensitive=show) for e in items], total=total, skip=skip, limit=limit
    )


@router.get("/{employee_id}", response_model=EmployeeRead)
def get_employee(employee_id: int, service: EmployeeServiceDep, current: CurrentEmployee):
    return EmployeeRead.from_model(service.get(employee_id), show_sensitive=can_view_sensitive(current))


@router.get("/{employee_id}/clients", response_model=list[ClientRead])
def list_employee_clients(employee_id: int, service: EmployeeServiceDep, current: CurrentEmployee):
    show = can_view_sensitive(current)
    return [ClientRead.from_model(c, show_sensitive=show) for c in service.list_clients(employee_id)]


@router.post(
    "/{employee_id}/clients",
    response_model=ClientRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_levels(*WRITE_LEVELS))],
)
def link_client(employee_id: int, data: EmployeeClientLink, service: EmployeeServiceDep, current: CurrentEmployee):
    client = service.link_client(employee_id, data.client_id)
    return ClientRead.from_model(client, show_sensitive=can_view_sensitive(current))


@router.delete(
    "/{employee_id}/clients/{client_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_levels(*WRITE_LEVELS))],
)
def unlink_client(employee_id: int, client_id: int, service: EmployeeServiceDep):
    service.unlink_client(employee_id, client_id)
