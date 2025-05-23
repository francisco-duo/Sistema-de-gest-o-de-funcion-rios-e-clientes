from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    cnpj = Column(String, unique=True, index=True)

    employees = relationship(
        "Employee",
        secondary="employee_client_association_table",
        back_populates="clients",
    )

    def __repr__(self):
        return f"<Client(id={self.id}, name={self.name}, email={self.email}, cnpj={self.cnpj})>"
