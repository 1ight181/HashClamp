from app.domain.security import PasswordHasher
from app.infrastructure.security.security import PwdlibPasswordHasher


def get_password_hasher() -> PasswordHasher:
    return PwdlibPasswordHasher()