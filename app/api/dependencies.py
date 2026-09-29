from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.models import Employee, EmployeeLevel
from app.services.auth_service import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

DbSession = Annotated[Session, Depends(get_db)]

# Níveis que podem criar clientes e vincular/desvincular clientes
WRITE_LEVELS = (EmployeeLevel.PLENO, EmployeeLevel.SENIOR, EmployeeLevel.ADMIN)


def get_current_employee(token: Annotated[str, Depends(oauth2_scheme)], db: DbSession) -> Employee:
    employee = AuthService(db).get_employee_from_token(token)
    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return employee


CurrentEmployee = Annotated[Employee, Depends(get_current_employee)]


def require_levels(*levels: EmployeeLevel):
    """Cria uma dependência que só deixa passar funcionários com um dos níveis informados."""

    def dependency(current: CurrentEmployee) -> Employee:
        if current.level not in levels:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Seu nível de acesso não permite esta operação.",
            )
        return current

    return dependency


def can_view_sensitive(employee: Employee) -> bool:
    """Só ADMIN recebe CPF e e-mail sem máscara."""
    return employee.level == EmployeeLevel.ADMIN
