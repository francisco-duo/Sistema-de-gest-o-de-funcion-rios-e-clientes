import itertools
import os

# Definidas antes de importar o app: os módulos de config leem o ambiente no import
os.environ["DATABASE_URL"] = "sqlite://"
os.environ["SECRET_KEY"] = "chave-secreta-usada-apenas-nos-testes-automatizados"

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import create_engine  # noqa: E402
from sqlalchemy.orm import Session, sessionmaker  # noqa: E402
from sqlalchemy.pool import StaticPool  # noqa: E402

from app.api.main import app  # noqa: E402
from app.core.database import Base, get_db  # noqa: E402
from app.core.models import Client, Employee, EmployeeLevel  # noqa: E402
from app.core.security import create_access_token, hash_password  # noqa: E402

DEFAULT_PASSWORD = "senha-de-teste-123"


@pytest.fixture
def db() -> Session:
    """Banco SQLite em memória, novo a cada teste."""
    # StaticPool: todas as conexões usam o mesmo banco em memória
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    with sessionmaker(bind=engine, autoflush=False)() as session:
        yield session
    engine.dispose()


@pytest.fixture
def client(db: Session) -> TestClient:
    """TestClient do FastAPI usando o banco em memória do teste."""
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def make_employee(db: Session):
    counter = itertools.count(1)

    def _make(level: EmployeeLevel = EmployeeLevel.JUNIOR, password: str = DEFAULT_PASSWORD, **fields) -> Employee:
        n = next(counter)
        employee = Employee(
            name=fields.pop("name", f"Funcionário {n}"),
            email=fields.pop("email", f"funcionario{n}@empresa.com"),
            cpf=fields.pop("cpf", f"{n:011d}"),
            password_hash=hash_password(password),
            level=level,
            **fields,
        )
        db.add(employee)
        db.commit()
        return employee

    return _make


@pytest.fixture
def make_client(db: Session):
    counter = itertools.count(1)

    def _make(**fields) -> Client:
        n = next(counter)
        client = Client(
            name=fields.pop("name", f"Cliente {n}"),
            email=fields.pop("email", f"contato{n}@cliente.com"),
            cnpj=fields.pop("cnpj", f"{n:014d}"),
            **fields,
        )
        db.add(client)
        db.commit()
        return client

    return _make


def auth_headers(employee: Employee) -> dict[str, str]:
    return {"Authorization": f"Bearer {create_access_token(str(employee.id))}"}


@pytest.fixture
def headers_for(make_employee):
    """Cria um funcionário do nível informado e devolve os headers com o token dele."""

    def _headers(level: EmployeeLevel) -> dict[str, str]:
        return auth_headers(make_employee(level=level))

    return _headers
