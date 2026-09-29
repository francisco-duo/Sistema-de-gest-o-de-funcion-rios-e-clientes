from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_serializer, field_validator

from app.utils.documents import normalize_document
from app.utils.masks import format_cnpj, mask_email


class ClientCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    cnpj: str = Field(examples=["12.345.678/0001-90"])

    @field_validator("name")
    @classmethod
    def strip_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Nome não pode ser vazio.")
        return value

    @field_validator("cnpj")
    @classmethod
    def validate_cnpj(cls, value: str) -> str:
        return normalize_document(value, 14, "CNPJ")


class ClientRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    cnpj: str

    @field_serializer("email")
    def serialize_email(self, value: str) -> str:
        return mask_email(value)

    @field_serializer("cnpj")
    def serialize_cnpj(self, value: str) -> str:
        return format_cnpj(value)
