from sqlalchemy import Table, Column, Integer, ForeignKey, String

from app.core.database import Base

employee_client_association_table = Table(
    "employee_client",
    Base.metadata,
    Column("employee_id", Integer, ForeignKey("employees.id"), primary_key=True),
    Column("client_id", Integer, ForeignKey("clients.id"), primary_key=True),
)