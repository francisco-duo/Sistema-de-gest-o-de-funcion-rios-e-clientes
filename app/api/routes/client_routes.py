from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.client_schema import ClientCreate, ClientRead
from app.schemas.pagination import Page
from app.services.client_service import ClientService

router = APIRouter(prefix="/clients", tags=["Clientes"])


def get_client_service(db: Session = Depends(get_db)) -> ClientService:
    return ClientService(db)


ClientServiceDep = Annotated[ClientService, Depends(get_client_service)]


@router.post("", response_model=ClientRead, status_code=status.HTTP_201_CREATED)
def create_client(data: ClientCreate, service: ClientServiceDep):
    return service.create(data)


@router.get("", response_model=Page[ClientRead])
def list_clients(
    service: ClientServiceDep,
    name: Annotated[str | None, Query(description="Filtra pelo nome (contém)")] = None,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
):
    items, total = service.list_paginated(name=name, skip=skip, limit=limit)
    return Page(items=items, total=total, skip=skip, limit=limit)


@router.get("/{client_id}", response_model=ClientRead)
def get_client(client_id: int, service: ClientServiceDep):
    return service.get(client_id)
