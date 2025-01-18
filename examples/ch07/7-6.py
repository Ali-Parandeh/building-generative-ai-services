# main.py

from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from database import DBSessionDep
from entities import Conversation
from schemas import ConversationIn, ConversationOut

app = FastAPI()


async def get_conversation(conversation_id: int, session: DBSessionDep) -> Conversation:
    async with session.begin():
        result = await session.execute(
            select(Conversation).where(Conversation.id == conversation_id)
        )
        conversation = result.scalars().first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


GetConversationDep = Annotated[Conversation, Depends(get_conversation)]


@app.get("/conversations")
async def list_conversations_controller(
    session: DBSessionDep, skip: int = 0, take: int = 100
) -> list[ConversationOut]:
    async with session.begin():
        result = await session.execute(select(Conversation).offset(skip).limit(take))
    return [ConversationOut.model_validate(conversation) for conversation in result.scalars().all()]


@app.get("/conversations/{id}")
async def get_conversation_controller(conversation: GetConversationDep) -> ConversationOut:
    return ConversationOut.model_validate(conversation)


@app.post("/conversations", status_code=201)
async def create_conversation_controller(
    conversation: ConversationIn, session: DBSessionDep
) -> ConversationOut:
    new_conversation = Conversation(**conversation.model_dump())
    async with session.begin():
        session.add(new_conversation)
        await session.commit()
        await session.refresh(new_conversation)
    return ConversationOut.model_validate(new_conversation)


@app.delete("/conversations/{id}", status_code=204)
async def delete_conversation_controller(
    conversation: GetConversationDep, session: DBSessionDep
) -> None:
    async with session.begin():
        await session.delete(conversation)
        await session.commit()
