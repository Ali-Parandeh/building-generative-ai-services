import asyncio
from typing import Annotated

from loguru import logger
from pydantic import BaseModel, Field

...


class ModerationResponse(BaseModel):
    score: Annotated[int, Field(ge=1, le=5)]


async def g_eval_moderate_content(
    chat_response: str, threshold: int = 3
) -> bool:
    response = await LLMClient(guardrail_system_prompt).invoke(chat_response)
    g_eval_score = ModerationResponse(score=response).score
    return g_eval_score >= threshold


async def invoke_llm_with_guardrails(user_request):
    ...
    while True:
        ...
        if topical_guardrail_task in done:
            ...
        elif chat_task in done:
            chat_response = chat_task.result()
            has_passed_moderation = await g_eval_moderate_content(chat_response)
            if not has_passed_moderation:
                logger.warning(f"Moderation guardrail flagged")
                return (
                    "Sorry, we can't recommend specific "
                    "tools or technologies at this time"
                )
            return chat_response
        else:
            await asyncio.sleep(0.1)
