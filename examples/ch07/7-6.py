# main.py

from typing import Annotated

from database import DBSessionDep
from entities import Conversation
from fastapi import Depends, FastAPI, HTTPException, status
from schemas import ConversationCreate, ConversationOut, ConversationUpdate
from sqlalchemy import select

app = FastAPI()


async def get_conversation(
    conversation_id: int, session: DBSessionDep
) -> Conversation:
    async with session.begin():
        result = await session.execute(
            select(Conversation).where(Conversation.id == conversation_id)
        )
        conversation = result.scalars().first()
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )
    return conversation


GetConversationDep = Annotated[Conversation, Depends(get_conversation)]


@app.get("/conversations")
async def list_conversations_controller(
    session: DBSessionDep, skip: int = 0, take: int = 100
) -> list[ConversationOut]:
    async with session.begin():
        result = await session.execute(
            select(Conversation).offset(skip).limit(take)
        )
    return [
        ConversationOut.model_validate(conversation)
        for conversation in result.scalars().all()
    ]


@app.get("/conversations/{id}")
async def get_conversation_controller(
    conversation: GetConversationDep,
) -> ConversationOut:
    return ConversationOut.model_validate(conversation)


@app.post("/conversations", status_code=status.HTTP_201_CREATED)
async def create_conversation_controller(
    conversation: ConversationCreate, session: DBSessionDep
) -> ConversationOut:
    new_conversation = Conversation(**conversation.model_dump())
    async with session.begin():
        session.add(new_conversation)
        await session.commit()
        await session.refresh(new_conversation)
    return ConversationOut.model_validate(new_conversation)


@app.put("/conversations/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_conversation_controller(
    updated_conversation: ConversationUpdate,
    conversation: GetConversationDep,
    session: DBSessionDep,
) -> ConversationOut:
    for key, value in updated_conversation.model_dump().items():
        setattr(conversation, key, value)
    async with session.begin():
        await session.commit()
        await session.refresh(conversation)
    return ConversationOut.model_validate(conversation)


@app.delete("/conversations/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation_controller(
    conversation: GetConversationDep, session: DBSessionDep
) -> None:
    async with session.begin():
        await session.delete(conversation)
        await session.commit()
