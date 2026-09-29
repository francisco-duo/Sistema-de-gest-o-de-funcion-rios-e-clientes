import pytest
from sqlalchemy import select

from app.core.models import Category, EmployeeLevel, Log
from app.services.employee_service import MAX_CLIENTS_JUNIOR
from tests.conftest import auth_headers

NEW_EMPLOYEE = {
    "name": "Ana Souza",
    "email": "ana.souza@empresa.com",
    "cpf": "123.456.789-01",
    "password": "senha-segura-123",
}


def test_admin_cria_funcionario(client, headers_for):
    response = client.post("/employees", json=NEW_EMPLOYEE, headers=headers_for(EmployeeLevel.ADMIN))

    assert response.status_code == 201
    data = response.json()
    assert data["level"] == "JUNIOR"
    assert data["cpf"] == "123.456.789-01"  # ADMIN vê o CPF completo
    assert "password" not in data and "password_hash" not in data


def test_funcionario_criado_consegue_fazer_login(client, headers_for):
    client.post("/employees", json=NEW_EMPLOYEE, headers=headers_for(EmployeeLevel.ADMIN))

    response = client.post(
        "/auth/token", data={"username": NEW_EMPLOYEE["email"], "password": NEW_EMPLOYEE["password"]}
    )

    assert response.status_code == 200


@pytest.mark.parametrize("level", [EmployeeLevel.JUNIOR, EmployeeLevel.PLENO, EmployeeLevel.SENIOR])
def test_so_admin_cria_funcionario(client, headers_for, level):
    response = client.post("/employees", json=NEW_EMPLOYEE, headers=headers_for(level))
    assert response.status_code == 403


def test_funcionario_com_cpf_duplicado_retorna_409(client, headers_for, make_employee):
    make_employee(cpf="12345678901")

    response = client.post("/employees", json=NEW_EMPLOYEE, headers=headers_for(EmployeeLevel.ADMIN))

    assert response.status_code == 409


@pytest.mark.parametrize(
    ("campo", "valor"),
    [("password", "curta"), ("level", "CHEFE"), ("cpf", "123")],
)
def test_funcionario_com_dados_invalidos_retorna_422(client, headers_for, campo, valor):
    payload = {**NEW_EMPLOYEE, campo: valor}
    assert client.post("/employees", json=payload, headers=headers_for(EmployeeLevel.ADMIN)).status_code == 422


def test_categoria_inexistente_retorna_404(client, headers_for):
    payload = {**NEW_EMPLOYEE, "category_id": 99}
    assert client.post("/employees", json=payload, headers=headers_for(EmployeeLevel.ADMIN)).status_code == 404


def test_listar_funcionarios_filtra_por_nivel_e_categoria(client, db, make_employee):
    category = Category(name="Vendas")
    viewer = make_employee(level=EmployeeLevel.JUNIOR)
    make_employee(level=EmployeeLevel.SENIOR, category=category)
    make_employee(level=EmployeeLevel.SENIOR)

    by_level = client.get("/employees", params={"level": "SENIOR"}, headers=auth_headers(viewer)).json()
    by_category = client.get("/employees", params={"category_id": category.id}, headers=auth_headers(viewer)).json()

    assert by_level["total"] == 2
    assert by_category["total"] == 1


def test_cpf_mascarado_para_quem_nao_e_admin(client, make_employee):
    viewer = make_employee(level=EmployeeLevel.SENIOR)
    other = make_employee(cpf="98765432100")

    data = client.get(f"/employees/{other.id}", headers=auth_headers(viewer)).json()

    assert data["cpf"] == "***.654.321-**"


class TestVinculos:
    def test_vincular_listar_e_desvincular(self, client, db, make_employee, make_client):
        manager = make_employee(level=EmployeeLevel.PLENO)
        employee = make_employee()
        customer = make_client()
        headers = auth_headers(manager)
        url = f"/employees/{employee.id}/clients"

        assert client.post(url, json={"client_id": customer.id}, headers=headers).status_code == 201
        assert [c["id"] for c in client.get(url, headers=headers).json()] == [customer.id]
        assert client.delete(f"{url}/{customer.id}", headers=headers).status_code == 204
        assert client.get(url, headers=headers).json() == []

        actions = db.scalars(select(Log.action).where(Log.action.in_(["LINK_CLIENT", "UNLINK_CLIENT"]))).all()
        assert actions == ["LINK_CLIENT", "UNLINK_CLIENT"]

    def test_junior_nao_pode_vincular(self, client, make_employee, make_client):
        junior = make_employee()
        response = client.post(
            f"/employees/{junior.id}/clients", json={"client_id": make_client().id}, headers=auth_headers(junior)
        )
        assert response.status_code == 403

    def test_limite_de_clientes_para_junior(self, client, make_employee, make_client, headers_for):
        junior = make_employee(level=EmployeeLevel.JUNIOR)
        headers = headers_for(EmployeeLevel.ADMIN)
        url = f"/employees/{junior.id}/clients"

        for _ in range(MAX_CLIENTS_JUNIOR):
            assert client.post(url, json={"client_id": make_client().id}, headers=headers).status_code == 201

        response = client.post(url, json={"client_id": make_client().id}, headers=headers)

        assert response.status_code == 422
        assert "no máximo" in response.json()["detail"]

    def test_senior_nao_tem_limite(self, client, make_employee, make_client, headers_for):
        senior = make_employee(level=EmployeeLevel.SENIOR)
        headers = headers_for(EmployeeLevel.ADMIN)

        for _ in range(MAX_CLIENTS_JUNIOR + 1):
            response = client.post(
                f"/employees/{senior.id}/clients", json={"client_id": make_client().id}, headers=headers
            )
            assert response.status_code == 201

    def test_vinculo_duplicado_retorna_409(self, client, make_employee, make_client, headers_for):
        employee = make_employee()
        customer = make_client()
        headers = headers_for(EmployeeLevel.ADMIN)
        url = f"/employees/{employee.id}/clients"

        client.post(url, json={"client_id": customer.id}, headers=headers)

        assert client.post(url, json={"client_id": customer.id}, headers=headers).status_code == 409

    @pytest.mark.parametrize(("employee_id", "client_id"), [(999, 1), (1, 999)])
    def test_vinculo_com_inexistente_retorna_404(
        self, client, make_employee, make_client, headers_for, employee_id, client_id
    ):
        make_employee()
        make_client()
        response = client.post(
            f"/employees/{employee_id}/clients", json={"client_id": client_id}, headers=headers_for(EmployeeLevel.ADMIN)
        )
        assert response.status_code == 404

    def test_desvincular_cliente_nao_vinculado_retorna_404(self, client, make_employee, make_client, headers_for):
        employee = make_employee()
        customer = make_client()
        response = client.delete(
            f"/employees/{employee.id}/clients/{customer.id}", headers=headers_for(EmployeeLevel.ADMIN)
        )
        assert response.status_code == 404
