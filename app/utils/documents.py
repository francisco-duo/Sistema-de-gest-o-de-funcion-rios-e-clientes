import re


def only_digits(value: str) -> str:
    """Remove tudo que não for dígito (ex.: '123.456.789-01' -> '12345678901')."""
    return re.sub(r"\D", "", value)


def normalize_document(value: str, length: int, name: str) -> str:
    """Normaliza CPF/CNPJ para apenas dígitos e valida a quantidade."""
    digits = only_digits(value)
    if len(digits) != length:
        raise ValueError(f"{name} deve ter {length} dígitos.")
    return digits
