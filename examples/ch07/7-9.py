# routers/conversations.py

from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status

...  # Other imports
from repositories import ConversationRepository

...  # Other controllers and dependency implementations

router = APIRouter(prefix="/conversations")


async def get_conversation(conversation_id: int, session: SessionDep) -> Conversation:
    conversation = await ConversationRepository(session).get(conversation_id)
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    return conversation


GetConversationDep = Annotated[Conversation, Depends(get_conversation)]


@router.get("")
async def list_conversations_controller(
    session: SessionDep, skip: int = 0, take: int = 100
) -> list[ConversationOut]:
    conversations = await ConversationRepository(session).list(skip, take)
    return [ConversationOut.model_validate(c) for c in conversations]


@router.get("/{id}")
async def get_conversation_controller(conversation: GetConversationDep) -> ConversationOut:
    return ConversationOut.model_validate(conversation)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_conversation_controller(
    conversation: ConversationCreate, session: SessionDep
) -> ConversationOut:
    new_conversation = await ConversationRepository(session).create(conversation)
    return ConversationOut.model_validate(new_conversation)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_conversation_controller(
    conversation: GetConversationDep, updated_conversation: ConversationUpdate, session: SessionDep
) -> ConversationOut:
    updated_conversation = await ConversationRepository(session).update(
        conversation.id, updated_conversation
    )
    return ConversationOut.model_validate(updated_conversation)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation_controller(
    conversation: GetConversationDep, session: SessionDep
) -> None:
    await ConversationRepository(session).delete(conversation.id)


# main.py

from fastapi import FastAPI
from routers.conversations import router as conversations_router

app = FastAPI()

app.include_router(conversations_router)
