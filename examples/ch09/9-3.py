import asyncio
from typing import Annotated

from fastapi import Depends
from loguru import logger

...


async def invoke_llm_with_guardrails(user_query: str) -> str:
    topical_guardrail_task = asyncio.create_task(is_topic_allowed(user_query))
    chat_task = asyncio.create_task(llm_client.invoke(user_query))

    while True:
        done, _ = await asyncio.wait(
            [topical_guardrail_task, chat_task],
            return_when=asyncio.FIRST_COMPLETED,
        )
        if topical_guardrail_task in done:
            topic_allowed = topical_guardrail_task.result()
            if not topic_allowed:
                chat_task.cancel()
                logger.warning("Topical guardrail triggered")
                return "Sorry, I can only talk about building GenAI services with FastAPI"
            elif chat_task in done:
                return chat_task.result()
        else:
            await asyncio.sleep(0.1)


@router.post("/text/generate")
async def generate_text_controller(
    response: Annotated[str, Depends(invoke_llm_with_guardrails)]
) -> str:
    return response
