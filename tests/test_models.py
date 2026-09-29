import pytest
from sqlalchemy.orm import configure_mappers

from app.core.models import Category, EmployeeLevel


def test_mappers_configuram_sem_erro():
    # Teria pegado os erros de relacionamento ("User" inexistente e `secondary` errado)
    configure_mappers()


def test_relacionamento_categoria_funcionario(db, make_employee):
    category = Category(name="Desenvolvimento")
    employee = make_employee(category=category)

    assert employee.category is category
    assert category.employees == [employee]


def test_relacionamento_n_para_n_funcionario_cliente(db, make_employee, make_client):
    employee = make_employee()
    client = make_client()

    employee.clients.append(client)
    db.commit()

    assert client.employees == [employee]


def test_nivel_padrao_e_junior(make_employee):
    assert make_employee().level == EmployeeLevel.JUNIOR


def test_cpf_e_cnpj_sao_salvos_so_com_digitos(make_employee, make_client):
    assert make_employee(cpf="123.456.789-01").cpf == "12345678901"
    assert make_client(cnpj="12.345.678/0001-90").cnpj == "12345678000190"


@pytest.mark.parametrize("cpf", ["123", "123.456.789-012"])
def test_cpf_com_tamanho_errado_gera_erro(make_employee, cpf):
    with pytest.raises(ValueError, match="CPF deve ter 11 dígitos"):
        make_employee(cpf=cpf)
