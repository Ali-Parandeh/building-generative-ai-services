# stream.py

import asyncio
from typing import AsyncGenerator
from huggingface_hub import AsyncInferenceClient

client = AsyncInferenceClient("http://localhost:8080")


async def chat_stream(prompt: str) -> AsyncGenerator[str, None]:
    stream = await client.text_generation(prompt, stream=True)
    async for token in stream:
        yield token
        await asyncio.sleep(0.05)
