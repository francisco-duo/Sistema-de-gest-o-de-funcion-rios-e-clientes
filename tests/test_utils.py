import pytest

from app.utils.documents import normalize_document, only_digits
from app.utils.masks import format_cnpj, format_cpf, mask_cpf, mask_email


def test_only_digits():
    assert only_digits("12.345.678/0001-90") == "12345678000190"


def test_normalize_document_valida_tamanho():
    assert normalize_document("123.456.789-01", 11, "CPF") == "12345678901"
    with pytest.raises(ValueError, match="CNPJ deve ter 14 dígitos"):
        normalize_document("123", 14, "CNPJ")


def test_mascaras_de_cpf_e_cnpj():
    assert mask_cpf("12345678901") == "***.456.789-**"
    assert format_cpf("12345678901") == "123.456.789-01"
    assert format_cnpj("12345678000190") == "12.345.678/0001-90"


@pytest.mark.parametrize(
    ("email", "esperado"),
    [
        ("francisco@gmail.com", "f*******o@gmail.com"),
        ("ab@x.com", "a*@x.com"),
        ("a@x.com", "a@x.com"),
    ],
)
def test_mask_email(email, esperado):
    assert mask_email(email) == esperado
