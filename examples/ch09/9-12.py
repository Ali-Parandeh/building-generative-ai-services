# stream.py


# stream.py

import asyncio
from typing import AsyncGenerator


class AzureOpenAIChatClient:
    def __init__(self, throttle_rate=0.5):
        self.aclient = ...
        self.throttle_rate = throttle_rate

    async def chat_stream(
        self, prompt: str, mode: str = "sse", model: str = "gpt-3.5-turbo"
    ) -> AsyncGenerator[str, None]:
        stream = ...  # OpenAI chat completion stream
        async for chunk in stream:
            await asyncio.sleep(self.throttle_rate)
            if chunk.choices[0].delta.content is not None:
                yield (
                    f"data: {chunk.choices[0].delta.content}\n\n"
                    if mode == "sse"
                    else chunk.choices[0].delta.content
                )
                await asyncio.sleep(0.05)

        if mode == "sse":
            yield f"data: [DONE]\n\n"
