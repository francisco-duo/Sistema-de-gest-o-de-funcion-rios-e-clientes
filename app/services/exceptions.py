class ServiceError(Exception):
    """Erro de regra de negócio. As rotas convertem em resposta HTTP pelo status_code."""

    status_code = 400

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class NotFoundError(ServiceError):
    status_code = 404


class ConflictError(ServiceError):
    status_code = 409


class BusinessRuleError(ServiceError):
    status_code = 422
