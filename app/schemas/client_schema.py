from pydantic import BaseModel, EmailStr, Field, field_validator

from app.core.models import Client
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
    id: int
    name: str
    email: str
    cnpj: str

    @classmethod
    def from_model(cls, client: Client, *, show_sensitive: bool = False) -> "ClientRead":
        """Monta a resposta; o e-mail só vem completo quando `show_sensitive` é True (ADMIN)."""
        return cls(
            id=client.id,
            name=client.name,
            email=client.email if show_sensitive else mask_email(client.email),
            cnpj=format_cnpj(client.cnpj),
        )
