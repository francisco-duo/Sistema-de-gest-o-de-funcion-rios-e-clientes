from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from app.core.database import Base
from app.utils.documents import normalize_document

if TYPE_CHECKING:
    from app.core.models.employee_model import Employee


class Client(Base):
    __tablename__ = "clients"
    __table_args__ = (CheckConstraint("length(cnpj) = 14", name="ck_clients_cnpj_length"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    cnpj: Mapped[str] = mapped_column(String(14), unique=True, index=True)  # Apenas dígitos

    employees: Mapped[list["Employee"]] = relationship(
        secondary="employee_client",
        back_populates="clients",
    )

    @validates("cnpj")
    def validate_cnpj(self, key, value):
        return normalize_document(value, 14, "CNPJ")

    def __repr__(self):
        # CNPJ e e-mail ficam de fora para não vazarem em logs
        return f"<Client(id={self.id}, name={self.name})>"
