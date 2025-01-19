# services/auth.py

from fastapi.security import HTTPBearer
from passlib.context import CryptContext


class PasswordService:
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"])

    async def verify_password(self, password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(password, hashed_password)

    async def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)
