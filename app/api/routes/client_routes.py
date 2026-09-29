from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies import WRITE_LEVELS, CurrentEmployee, DbSession, can_view_sensitive, require_levels
from app.schemas.client_schema import ClientCreate, ClientRead
from app.schemas.pagination import Page
from app.services.client_service import ClientService

router = APIRouter(prefix="/clients", tags=["Clientes"])


def get_client_service(db: DbSession, current: CurrentEmployee) -> ClientService:
    return ClientService(db, actor=current)


ClientServiceDep = Annotated[ClientService, Depends(get_client_service)]


@router.post(
    "",
    response_model=ClientRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_levels(*WRITE_LEVELS))],
)
def create_client(data: ClientCreate, service: ClientServiceDep, current: CurrentEmployee):
    client = service.create(data)
    return ClientRead.from_model(client, show_sensitive=can_view_sensitive(current))


@router.get("", response_model=Page[ClientRead])
def list_clients(
    service: ClientServiceDep,
    current: CurrentEmployee,
    name: Annotated[str | None, Query(description="Filtra pelo nome (contém)")] = None,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
):
    items, total = service.list_paginated(name=name, skip=skip, limit=limit)
    show = can_view_sensitive(current)
    return Page(
        items=[ClientRead.from_model(c, show_sensitive=show) for c in items], total=total, skip=skip, limit=limit
    )


@router.get("/{client_id}", response_model=ClientRead)
def get_client(client_id: int, service: ClientServiceDep, current: CurrentEmployee):
    return ClientRead.from_model(service.get(client_id), show_sensitive=can_view_sensitive(current))
