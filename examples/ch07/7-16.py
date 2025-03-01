from entities import Conversation
from openai import AsyncClient
from repositories.conversations import ConversationRepository
from sqlalchemy.ext.asyncio import AsyncSession

async_client = AsyncClient(...)


async def create_conversation(
    initial_prompt: str, session: AsyncSession
) -> Conversation:
    completion = await async_client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Suggest a title for the conversation based on the user prompt",
            },
            {
                "role": "user",
                "content": initial_prompt,
            },
        ],
        model="gpt-3.5-turbo",
    )
    title = completion.choices[0].message.content
    conversation = Conversation(
        title=title,
        # add other conversation properties
        # ...
    )
    return await ConversationRepository(session).create(conversation)
