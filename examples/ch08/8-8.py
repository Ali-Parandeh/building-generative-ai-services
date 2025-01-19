# repositories.py

from entities import Token
from repositories.interfaces import Repository
from schemas import TokenCreate, TokenUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class TokenRepository(Repository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list(self, skip: int, take: int) -> list[Token]:
        async with self.session.begin():
            result = await self.session.execute(select(Token).offset(skip).limit(take))
        return [r for r in result.scalars().all()]

    async def get(self, token_id: int) -> Token | None:
        async with self.session.begin():
            result = await self.session.execute(select(Token).where(Token.id == token_id))
        return result.scalars().first()

    async def create(self, token: TokenCreate) -> Token:
        new_token = Token(**token.dict())
        async with self.session.begin():
            self.session.add(new_token)
            await self.session.commit()
            await self.session.refresh(new_token)
        return new_token

    async def update(self, token_id: int, updated_token: TokenUpdate) -> Token | None:
        token = await self.get(token_id)
        if not token:
            return None
        for key, value in updated_token.dict(exclude_unset=True).items():
            setattr(token, key, value)
        async with self.session.begin():
            await self.session.commit()
            await self.session.refresh(token)
        return token

    async def delete(self, token_id: int) -> None:
        token = await self.get(token_id)
        if not token:
            return
        async with self.session.begin():
            await self.session.delete(token)
            await self.session.commit()
