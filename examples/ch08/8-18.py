# routes/auth.py

from typing import Annotated

import aiohttp
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer()
HTTPBearerDep = Annotated[HTTPAuthorizationCredentials, Depends(security)]

router = APIRouter()


async def get_user_info(credentials: HTTPBearerDep) -> dict:
    try:
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {credentials.credentials}"}
            async with session.get(
                "https://api.github.com/user", headers=headers
            ) as resp:
                return await resp.json()
    except Exception as e:
        raise HTTPException(
            status_code=503, detail=f"Failed to obtain user info - Error: {e}"
        )


GetUserInfoDep = Annotated[dict, Depends(get_user_info)]


@router.get("/oauth/github/callback")
async def get_current_user_controller(user_info: GetUserInfoDep) -> dict:
    return user_info
