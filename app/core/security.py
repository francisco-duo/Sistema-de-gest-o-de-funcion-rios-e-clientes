from datetime import UTC, datetime, timedelta

import jwt
from pwdlib import PasswordHash

from app.core.configs import SECURITY_CONFIG

if not SECURITY_CONFIG["SECRET_KEY"]:
    raise ValueError(
        "A variável de ambiente SECRET_KEY não está definida. "
        'Gere uma com: python -c "import secrets; print(secrets.token_hex(32))"'
    )

password_hash = PasswordHash.recommended()  # Argon2

# Hash usado quando o e-mail não existe, para o login levar o mesmo tempo
# nos dois casos e não revelar quais e-mails estão cadastrados.
DUMMY_HASH = password_hash.hash("dummy-password")


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return password_hash.verify(password, hashed)


def create_access_token(subject: str) -> str:
    expire = datetime.now(UTC) + timedelta(minutes=SECURITY_CONFIG["ACCESS_TOKEN_EXPIRE_MINUTES"])
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, SECURITY_CONFIG["SECRET_KEY"], algorithm=SECURITY_CONFIG["ALGORITHM"])


def decode_access_token(token: str) -> str | None:
    """Retorna o `sub` do token, ou None se o token for inválido ou estiver expirado."""
    try:
        payload = jwt.decode(token, SECURITY_CONFIG["SECRET_KEY"], algorithms=[SECURITY_CONFIG["ALGORITHM"]])
    except jwt.InvalidTokenError:
        return None
    return payload.get("sub")
