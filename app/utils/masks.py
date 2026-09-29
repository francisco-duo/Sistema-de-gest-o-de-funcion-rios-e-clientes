def mask_cpf(cpf: str) -> str:
    """'12345678901' -> '***.456.789-**'"""
    return f"***.{cpf[3:6]}.{cpf[6:9]}-**"


def format_cpf(cpf: str) -> str:
    """'12345678901' -> '123.456.789-01'"""
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"


def mask_email(email: str) -> str:
    """'francisco@gmail.com' -> 'f*******o@gmail.com'"""
    local, _, domain = email.partition("@")
    if len(local) <= 2:
        masked = local[0] + "*" * (len(local) - 1)
    else:
        masked = local[0] + "*" * (len(local) - 2) + local[-1]
    return f"{masked}@{domain}"


def format_cnpj(cnpj: str) -> str:
    """'12345678000190' -> '12.345.678/0001-90'"""
    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
