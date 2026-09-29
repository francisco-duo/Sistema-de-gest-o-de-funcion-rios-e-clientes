from sqlalchemy.orm import Session

from app.core.models import Employee
from app.core.security import DUMMY_HASH, create_access_token, decode_access_token, verify_password
from app.repositories.employee_repository import EmployeeRepository


class AuthService:
    def __init__(self, db: Session):
        self.repository = EmployeeRepository(db)

    def authenticate(self, email: str, password: str) -> str | None:
        """Retorna um token de acesso se e-mail e senha estiverem corretos; senão, None."""
        employee = self.repository.get_by_email(email)
        if employee is None:
            verify_password(password, DUMMY_HASH)  # mesmo tempo de resposta de um e-mail existente
            return None
        if not verify_password(password, employee.password_hash):
            return None
        return create_access_token(str(employee.id))

    def get_employee_from_token(self, token: str) -> Employee | None:
        subject = decode_access_token(token)
        if subject is None or not subject.isdigit():
            return None
        return self.repository.get_by_id(int(subject))
