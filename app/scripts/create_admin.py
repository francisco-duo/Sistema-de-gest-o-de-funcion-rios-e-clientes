"""Cria o primeiro funcionário ADMIN (as rotas da API exigem login).

Uso:
    python -m app.scripts.create_admin --name "Seu Nome" --email voce@empresa.com --cpf 12345678901
A senha é pedida no terminal, sem aparecer na tela.
"""

import argparse
import getpass
import sys

from pydantic import ValidationError

from app.core.database import SessionLocal
from app.core.models import EmployeeLevel
from app.schemas.employee_schema import EmployeeCreate
from app.services.employee_service import EmployeeService
from app.services.exceptions import ServiceError


def main() -> int:
    parser = argparse.ArgumentParser(description="Cria um funcionário ADMIN.")
    parser.add_argument("--name", required=True)
    parser.add_argument("--email", required=True)
    parser.add_argument("--cpf", required=True)
    args = parser.parse_args()

    password = getpass.getpass("Senha (mínimo 8 caracteres): ")
    if password != getpass.getpass("Confirme a senha: "):
        print("As senhas não conferem.", file=sys.stderr)
        return 1

    try:
        data = EmployeeCreate(
            name=args.name,
            email=args.email,
            cpf=args.cpf,
            password=password,
            level=EmployeeLevel.ADMIN,
        )
    except ValidationError as exc:
        for error in exc.errors():
            print(f"{error['loc'][0]}: {error['msg']}", file=sys.stderr)
        return 1

    with SessionLocal() as db:
        try:
            employee = EmployeeService(db).create(data)
        except ServiceError as exc:
            print(exc.message, file=sys.stderr)
            return 1

    print(f"ADMIN criado com id {employee.id}. Faça login em POST /auth/token.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
