from fastapi import FastAPI

from app.core.database import Base, engine
from app.core.models import(
    category_model,
    client_model,
    employee_model,
    employee_client_model,
    log_model
)

Base.metadata.create_all(bind=engine)

app: FastAPI = FastAPI(
    title="Sistema de Gestão de Funcionários e Clientes",
    description="API para gerenciar funcionários e clientes",
    version="0.1.0",
    openapi_tags=[
        {
            "name": "Funcionários",
            "description": "Operações relacionadas a funcionários",
        },
        {
            "name": "Clientes",
            "description": "Operações relacionadas a clientes",
        },
    ]
)
