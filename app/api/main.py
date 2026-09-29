from fastapi import FastAPI

from app.core import models  # noqa: F401 - registra os models; o schema é gerenciado pelo Alembic

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
