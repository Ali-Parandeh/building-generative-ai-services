# services/auth.py

from datetime import UTC, datetime, timedelta

from exceptions import UnauthorizedException
from jose import JWTError, jwt
from pydantic import UUID4
from repositories import TokenRepository
from schemas import TokenCreate, TokenUpdate


class TokenService(TokenRepository):
    secret_key = "your_secret_key"
    algorithm = "HS256"
    expires_in_minutes = 60

    async def create_access_token(self, data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(UTC) + expires_delta
        else:
            expire = datetime.now(UTC) + timedelta(minutes=self.expires_in_minutes)
        token_id = await self.create(TokenCreate(expires_at=expire))
        to_encode.update({"exp": expire, "iss": "your_service_name", "sub": token_id})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    async def deactivate(self, token_id: UUID4) -> None:
        await self.update(TokenUpdate(id=token_id, is_active=False))

    def decode(self, encoded_token: str) -> dict:
        try:
            return jwt.decode(encoded_token, self.secret_key, algorithms=[self.algorithm])
        except JWTError:
            raise UnauthorizedException

    async def validate(self, token_id: UUID4) -> bool:
        return (token := await self.get(token_id)) is not None and token.is_active
