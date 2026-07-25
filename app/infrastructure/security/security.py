from pwdlib import PasswordHash


class PwdlibPasswordHasher:
    def __init__(self):
        self._hash = PasswordHash.recommended()

    def hash(self, password: str) -> str:
        return self._hash.hash(password)

    def verify(self, password: str, hashed_password: str) -> bool:
        return self._hash.verify(password, hashed_password)
