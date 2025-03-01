# routes/auth.py

from typing import Annotated

import aiohttp
from fastapi import Depends, HTTPException
from loguru import logger

...

client_id = "your_client_id"
client_secret = "your_client_secret"


async def exchange_grant_with_access_token(code: str) -> str:
    try:
        body = {
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://github.com/login/oauth/access_token",
                json=body,
                headers=headers,
            ) as resp:
                access_token_data = await resp.json()
    except Exception as e:
        logger.warning(f"Failed to fetch the access token. Error: {e}")
        raise HTTPException(
            status_code=503, detail="Failed to fetch access token"
        )

    if not access_token_data:
        raise HTTPException(
            status_code=503, detail="Failed to obtain access token"
        )

    return access_token_data.get("access_token", "")


ExchangeCodeTokenDep = Annotated[str, Depends(exchange_grant_with_access_token)]
