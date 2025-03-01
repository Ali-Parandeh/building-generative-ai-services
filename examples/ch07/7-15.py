# main.py

from itertools import tee

from database import DBSessionDep
from entities import Message
from fastapi import BackgroundTasks, Depends, FastAPI
from fastapi.responses import StreamingResponse
from repositories.conversations import Conversation
from repositories.messages import MessageRepository
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()


async def store_message(
    prompt_content: str,
    response_content: str,
    conversation_id: int,
    session: AsyncSession,
) -> None:
    message = Message(
        conversation_id=conversation_id,
        prompt_content=prompt_content,
        response_content=response_content,
    )
    await MessageRepository(session).create(message)


@app.get("/text/generate/stream")
async def stream_llm_controller(
    prompt: str,
    background_task: BackgroundTasks,
    session: DBSessionDep,
    conversation: Conversation = Depends(get_conversation),
) -> StreamingResponse:
    # Invoke LLM and obtain the response stream
    ...
    stream_1, stream_2 = tee(response_stream)
    background_task.add_task(
        store_message, prompt, "".join(stream_1), conversation.id, session
    )
    return StreamingResponse(stream_2)
