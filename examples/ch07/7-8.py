# repositories/conversations.py

from entities import Conversation
from repositories.interfaces import Repository
from schemas import ConversationCreate, ConversationUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class ConversationRepository(Repository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list(self, skip: int, take: int) -> list[Conversation]:
        async with self.session.begin():
            result = await self.session.execute(
                select(Conversation).offset(skip).limit(take)
            )
        return [r for r in result.scalars().all()]

    async def get(self, conversation_id: int) -> Conversation | None:
        async with self.session.begin():
            result = await self.session.execute(
                select(Conversation).where(Conversation.id == conversation_id)
            )
        return result.scalars().first()

    async def create(self, conversation: ConversationCreate) -> Conversation:
        new_conversation = Conversation(**conversation.model_dump())
        async with self.session.begin():
            self.session.add(new_conversation)
            await self.session.commit()
            await self.session.refresh(new_conversation)
        return new_conversation

    async def update(
        self, conversation_id: int, updated_conversation: ConversationUpdate
    ) -> Conversation | None:
        conversation = await self.get(conversation_id)
        if not conversation:
            return None
        for key, value in updated_conversation.model_dump().items():
            setattr(conversation, key, value)
        async with self.ession.begin():
            await self.session.commit()
            await self.session.refresh(conversation)
        return conversation

    async def delete(self, conversation_id: int) -> None:
        conversation = await self.get(conversation_id)
        if not conversation:
            return
        async with self.session.begin():
            await self.session.delete(conversation)
            await self.session.commit()
