from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_serializer, field_validator

from app.core.models import EmployeeLevel
from app.utils.documents import normalize_document
from app.utils.masks import mask_cpf, mask_email


class EmployeeCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    cpf: str = Field(examples=["123.456.789-01"])
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
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    cpf: str
    level: EmployeeLevel
    category_id: int | None

    @field_serializer("email")
    def serialize_email(self, value: str) -> str:
        return mask_email(value)

    @field_serializer("cpf")
    def serialize_cpf(self, value: str) -> str:
        return mask_cpf(value)


class EmployeeClientLink(BaseModel):
    client_id: int
