from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.core.models.employee_model import Employee


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(String(255))

    employees: Mapped[list["Employee"]] = relationship(back_populates="category")

    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name})>"
