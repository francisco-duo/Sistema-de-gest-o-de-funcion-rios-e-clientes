import enum
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from app.core.database import Base
from app.utils.documents import normalize_document

if TYPE_CHECKING:
    from app.core.models.category_model import Category
    from app.core.models.client_model import Client


class EmployeeLevel(str, enum.Enum):
    JUNIOR = "JUNIOR"
    PLENO = "PLENO"
    SENIOR = "SENIOR"
    ADMIN = "ADMIN"


class Employee(Base):
    __tablename__ = 'employees'
    __table_args__ = (
        CheckConstraint("length(cpf) = 11", name="ck_employees_cpf_length"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    cpf: Mapped[str] = mapped_column(String(11), unique=True, index=True)  # Apenas dígitos
    level: Mapped[EmployeeLevel] = mapped_column(
        Enum(EmployeeLevel, native_enum=False, length=20, create_constraint=True, name="ck_employees_level"),
        default=EmployeeLevel.JUNIOR,
        server_default=EmployeeLevel.JUNIOR.value,
    )

    category_id: Mapped[int | None] = mapped_column(ForeignKey('categories.id'))
    category: Mapped["Category | None"] = relationship(back_populates="employees")

    clients: Mapped[list["Client"]] = relationship(
        secondary="employee_client",
        back_populates="employees",
    )

    @validates("cpf")
    def validate_cpf(self, key, value):
        return normalize_document(value, 11, "CPF")

    def __repr__(self):
        # CPF e e-mail ficam de fora para não vazarem em logs
        return f"<Employee(id={self.id}, name={self.name}, level={self.level})>"
