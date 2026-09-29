from datetime import UTC, datetime, timedelta

import jwt
import pytest

from app.core.configs import SECURITY_CONFIG
from app.core.models import EmployeeLevel
from tests.conftest import DEFAULT_PASSWORD, auth_headers


def login(client, email, password):
    return client.post("/auth/token", data={"username": email, "password": password})


def test_login_com_credenciais_corretas_retorna_token(client, make_employee):
    employee = make_employee()

    response = login(client, employee.email, DEFAULT_PASSWORD)

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    token = response.json()["access_token"]
    assert client.get("/auth/me", headers={"Authorization": f"Bearer {token}"}).json()["id"] == employee.id


@pytest.mark.parametrize(
    ("email", "password"),
    [("funcionario1@empresa.com", "senha-errada"), ("nao@existe.com", DEFAULT_PASSWORD)],
)
def test_login_com_credenciais_erradas_retorna_401(client, make_employee, email, password):
    make_employee()

    response = login(client, email, password)

    assert response.status_code == 401
    assert response.json()["detail"] == "E-mail ou senha incorretos."


def test_senha_e_salva_com_hash(make_employee):
    assert make_employee().password_hash.startswith("$argon2")


@pytest.mark.parametrize("path", ["/auth/me", "/clients", "/employees", "/clients/1", "/employees/1/clients"])
def test_rotas_exigem_login(client, path):
    assert client.get(path).status_code == 401


def test_token_invalido_retorna_401(client):
    response = client.get("/auth/me", headers={"Authorization": "Bearer token-falso"})
    assert response.status_code == 401


def test_token_expirado_retorna_401(client, make_employee):
    employee = make_employee()
    expired = jwt.encode(
        {"sub": str(employee.id), "exp": datetime.now(UTC) - timedelta(minutes=1)},
        SECURITY_CONFIG["SECRET_KEY"],
        algorithm=SECURITY_CONFIG["ALGORITHM"],
    )

    response = client.get("/auth/me", headers={"Authorization": f"Bearer {expired}"})

    assert response.status_code == 401


def test_me_mascara_dados_para_quem_nao_e_admin(client, make_employee):
    employee = make_employee(level=EmployeeLevel.SENIOR, cpf="12345678901", email="maria.silva@empresa.com")

    data = client.get("/auth/me", headers=auth_headers(employee)).json()

    assert data["cpf"] == "***.456.789-**"
    assert data["email"] == "m*********a@empresa.com"
    assert "password" not in data and "password_hash" not in data
