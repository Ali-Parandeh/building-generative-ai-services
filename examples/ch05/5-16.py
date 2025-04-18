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
            response = await session.post(
                "http://localhost:8000/v1/chat", json=data, headers=headers
            )
            predictions = await response.json()
    except Exception as e:
        logger.error(f"Failed to obtain predictions from VLLM - Error: {e}")
        return "Failed to obtain predictions from VLLM - See server logs for more details"
    try:
        output = predictions["choices"][0]["message"]["content"]
        logger.debug(f"Generated text: {output}")
        return output
    except KeyError as e:
        logger.error(f"Failed to parse predictions from VLLM - Error: {e}")
        return "Failed to parse predictions from VLLM - See server logs for more details"
