from openai import AsyncOpenAI
from pydantic import BaseModel, Field

client = AsyncOpenAI()


class DocumentClassification(BaseModel):
    category: str = Field(..., description="The category of the classification")


async def get_document_classification(
    title: str,
) -> DocumentClassification | str | None:
    response = await client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "classify the provided document into the following: ...",
            },
            {"role": "user", "content": title},
        ],
        response_format=DocumentClassification,
    )

    message = response.choices[0].message
    return message.parsed if message.parsed is not None else message.refusal
