# stream.py

import asyncio
from typing import AsyncGenerator


class AzureOpenAIChatClient:
    def __init__(self):
        self.aclient = ...

    async def chat_stream(
        self, prompt: str, mode: str = "sse", model: str = "gpt-3.5-turbo"
    ) -> AsyncGenerator[str, None]:
        stream = ...  # OpenAI chat completion stream

        async for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield (
                    f"data: {chunk.choices[0].delta.content}\n\n"
                    if mode == "sse"
                    else chunk.choices[0].delta.content
                )
                await asyncio.sleep(0.05)
        if mode == "sse":
            yield f"data: [DONE]\n\n"
