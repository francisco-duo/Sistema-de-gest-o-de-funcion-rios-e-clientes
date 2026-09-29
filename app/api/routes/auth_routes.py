from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import CurrentEmployee, DbSession, can_view_sensitive
from app.schemas.auth_schema import Token
from app.schemas.employee_schema import EmployeeRead
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/token", response_model=Token)
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()], db: DbSession):
    """Login com e-mail (no campo `username`) e senha. Retorna um token JWT."""
    token = AuthService(db).authenticate(form.username, form.password)
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(access_token=token)


@router.get("/me", response_model=EmployeeRead)
def me(current: CurrentEmployee):
    return EmployeeRead.from_model(current, show_sensitive=can_view_sensitive(current))
