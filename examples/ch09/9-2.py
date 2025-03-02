import re
from typing import Annotated

from openai import AsyncOpenAI
from pydantic import AfterValidator, BaseModel, validate_call

guardrail_system_prompt = "..."


class LLMClient:
    def __init__(self, system_prompt: str):
        self.client = AsyncOpenAI()
        self.system_prompt = system_prompt

    async def invoke(self, user_query: str) -> str | None:
        response = await self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_query},
            ],
            temperature=0,
        )
        return response.choices[0].message.content


@validate_call
def check_classification_response(value: str | None) -> str:
    if value is None or not re.match(r"^(allowed|disallowed)$", value):
        raise ValueError("Invalid topical guardrail response received")
    return value


ClassificationResponse = Annotated[
    str | None, AfterValidator(check_classification_response)
]


class TopicalGuardResponse(BaseModel):
    classification: ClassificationResponse


async def is_topic_allowed(user_query: str) -> TopicalGuardResponse:
    response = await LLMClient(guardrail_system_prompt).invoke(user_query)
    return TopicalGuardResponse(classification=response)
