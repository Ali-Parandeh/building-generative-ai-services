# models.py

import os
import aiohttp
from loguru import logger


async def generate_text(prompt: str, temperature: float = 0.7) -> str:
    system_prompt = "You are an AI assistant"
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]
    data = {"temperature": temperature, "messages": messages}
    headers = {"Authorization": f"Bearer {os.environ.get('VLLM_API_KEY')}"}
    try:
        async with aiohttp.ClientSession() as session:
            predictions = await session.post(
                "http://localhost:8000/v1/chat", json=data, headers=headers
            )
    except Exception as e:
        logger.error(f"Failed to obtain predictions from VLLM - Error: {e}")
        return "Failed to obtain predictions from VLLM - See server logs for more details"
    output = predictions.choices[0].message.content
    logger.debug(f"Generated text: {output}")
    return output
