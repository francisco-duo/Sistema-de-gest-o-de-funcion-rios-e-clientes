from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.models.category_model import Category


class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    cpf = Column(String, unique=True, index=True)

    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("Category", back_populates="employees")

    clients = relationship(
        "Client",
        secondary="employee_client_association_table",
        back_populates="employees",
    )

    def __repr__(self):
        return f"<Employee(id={self.id}, name={self.name}, email={self.email}, cpf={self.cpf})>"
