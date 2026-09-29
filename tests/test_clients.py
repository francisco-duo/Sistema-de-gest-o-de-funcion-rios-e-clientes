import pytest
from sqlalchemy import select

from app.core.models import EmployeeLevel, Log
from tests.conftest import auth_headers

NEW_CLIENT = {"name": " ACME Ltda ", "email": "contato@acme.com", "cnpj": "12.345.678/0001-90"}


@pytest.mark.parametrize("level", [EmployeeLevel.PLENO, EmployeeLevel.SENIOR, EmployeeLevel.ADMIN])
def test_criar_cliente_permitido(client, headers_for, level):
    response = client.post("/clients", json=NEW_CLIENT, headers=headers_for(level))

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "ACME Ltda"
    assert data["cnpj"] == "12.345.678/0001-90"


def test_junior_nao_pode_criar_cliente(client, headers_for):
    response = client.post("/clients", json=NEW_CLIENT, headers=headers_for(EmployeeLevel.JUNIOR))
    assert response.status_code == 403


def test_criar_cliente_grava_log_com_autor(client, db, make_employee):
    author = make_employee(level=EmployeeLevel.PLENO)
    client_id = client.post("/clients", json=NEW_CLIENT, headers=auth_headers(author)).json()["id"]

    log = db.scalar(select(Log).where(Log.action == "CREATE_CLIENT"))
    assert log.record_id == client_id
    assert log.performed_by == f"employee:{author.id}"
    assert log.data == {"name": "ACME Ltda"}


@pytest.mark.parametrize(
    ("campo", "valor"),
    [("email", "contato@acme.com"), ("cnpj", "12345678000190")],
)
def test_cliente_duplicado_retorna_409(client, headers_for, make_client, campo, valor):
    make_client(email="contato@acme.com", cnpj="12345678000190")
    payload = {"name": "Outro", "email": "outro@x.com", "cnpj": "99999999000199", campo: valor}

    response = client.post("/clients", json=payload, headers=headers_for(EmployeeLevel.ADMIN))

    assert response.status_code == 409


@pytest.mark.parametrize(
    ("campo", "valor"),
    [("cnpj", "123"), ("email", "nao-e-email"), ("name", "   ")],
)
def test_cliente_com_dados_invalidos_retorna_422(client, headers_for, campo, valor):
    response = client.post("/clients", json={**NEW_CLIENT, campo: valor}, headers=headers_for(EmployeeLevel.ADMIN))
    assert response.status_code == 422


def test_listar_clientes_com_filtro_e_paginacao(client, headers_for, make_client):
    for name in ["Alfa", "Beta", "Alfa Dois", "Alfa Três"]:
        make_client(name=name)

    response = client.get("/clients", params={"name": "alfa", "limit": 2}, headers=headers_for(EmployeeLevel.JUNIOR))

    data = response.json()
    assert data["total"] == 3
    assert [c["name"] for c in data["items"]] == ["Alfa", "Alfa Dois"]


def test_cliente_inexistente_retorna_404(client, headers_for):
    assert client.get("/clients/999", headers=headers_for(EmployeeLevel.JUNIOR)).status_code == 404


@pytest.mark.parametrize(
    ("level", "email_esperado"),
    [(EmployeeLevel.ADMIN, "contato@acme.com"), (EmployeeLevel.SENIOR, "c*****o@acme.com")],
)
def test_email_do_cliente_so_aparece_completo_para_admin(client, headers_for, make_client, level, email_esperado):
    created = make_client(email="contato@acme.com")

    response = client.get(f"/clients/{created.id}", headers=headers_for(level))

    assert response.json()["email"] == email_esperado
