from pydantic import BaseModel, EmailStr, Field, field_validator

from app.core.models import Employee, EmployeeLevel
from app.utils.documents import normalize_document
from app.utils.masks import format_cpf, mask_cpf, mask_email


class EmployeeCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    cpf: str = Field(examples=["123.456.789-01"])
    password: str = Field(min_length=8, max_length=128)
    level: EmployeeLevel = EmployeeLevel.JUNIOR
    category_id: int | None = None

    @field_validator("name")
    @classmethod
    def strip_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Nome não pode ser vazio.")
        return value

    @field_validator("cpf")
    @classmethod
    def validate_cpf(cls, value: str) -> str:
        return normalize_document(value, 11, "CPF")


class EmployeeRead(BaseModel):
    id: int
    name: str
    email: str
    cpf: str
    level: EmployeeLevel
    category_id: int | None

    @classmethod
    def from_model(cls, employee: Employee, *, show_sensitive: bool = False) -> "EmployeeRead":
        """Monta a resposta; CPF e e-mail só vêm completos quando `show_sensitive` é True (ADMIN)."""
        return cls(
            id=employee.id,
            name=employee.name,
            email=employee.email if show_sensitive else mask_email(employee.email),
            cpf=format_cpf(employee.cpf) if show_sensitive else mask_cpf(employee.cpf),
            level=employee.level,
            category_id=employee.category_id,
        )


class EmployeeClientLink(BaseModel):
    client_id: int
