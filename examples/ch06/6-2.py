# stream.py

import asyncio
import os
from typing import AsyncGenerator
from openai import AsyncAzureOpenAI


class AzureOpenAIChatClient:
    def __init__(self):
        self.aclient = AsyncAzureOpenAI(
            api_key=os.environ["OPENAI_API_KEY"],
            api_version=os.environ["OPENAI_API_VERSION"],
            azure_endpoint=os.environ["OPENAI_API_ENDPOINT"],
            azure_deployment=os.environ["OPENAI_API_DEPLOYMENT"],
        )

    async def chat_stream(
        self, prompt: str, model: str = "gpt-3.5-turbo"
    ) -> AsyncGenerator[str, None]:
        stream = await self.aclient.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=model,
            stream=True,
        )

        async for chunk in stream:
            yield f"data: {chunk.choices[0].delta.content or ''}\n\n"
            await asyncio.sleep(0.05)

        yield f"data: [DONE]\n\n"


azure_chat_client = AzureOpenAIChatClient()
