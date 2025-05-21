from sqlalchemy import Column, Integer, String, ForeignKey

from app.core.database import Base


class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    cpf = Column(String, unique=True, index=True)

    # Cargo -> Many To One