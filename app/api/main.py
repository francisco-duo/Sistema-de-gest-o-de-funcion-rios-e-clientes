from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routes import auth_routes, client_routes, employee_routes
from app.core import models  # noqa: F401 - registra os models; o schema é gerenciado pelo Alembic
from app.services.exceptions import ServiceError

app: FastAPI = FastAPI(
    title="Sistema de Gestão de Funcionários e Clientes",
    description="API para gerenciar funcionários e clientes",
    version="0.1.0",
    openapi_tags=[
        {
            "name": "Autenticação",
            "description": "Login e dados do funcionário autenticado",
        },
        {
            "name": "Funcionários",
            "description": "Operações relacionadas a funcionários",
        },
        {
            "name": "Clientes",
            "description": "Operações relacionadas a clientes",
        },
    ],
)


@app.exception_handler(ServiceError)
def service_error_handler(request: Request, exc: ServiceError) -> JSONResponse:
    """Converte erros de regra de negócio dos services em respostas HTTP."""
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


app.include_router(auth_routes.router)
app.include_router(employee_routes.router)
app.include_router(client_routes.router)
