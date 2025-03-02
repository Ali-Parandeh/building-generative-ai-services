# dependencies/auth.py

from typing import Annotated

from entities import User
from fastapi import APIRouter, Depends, HTTPException, status
from services.auth import AuthService

CurrentUserDep = Annotated[User, Depends(AuthService.get_current_user)]


async def has_role(user: CurrentUserDep, roles: list[str]) -> User:
    if user.role not in roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to perform this action",
        )
    return user


# routes/resource.py

router = APIRouter(
    dependencies=[Depends(AuthService.get_current_user)],
    prefix="/generate",
    tags=["Resource"],
)


@router.post(
    "/image",
    dependencies=[Depends(lambda user: has_role(user, ["ADMIN", "MODERATOR"]))],
)
async def generate_image_controller(): ...


@router.post(
    "/text", dependencies=[Depends(lambda user: has_role(user, ["EDITOR"]))]
)
async def generate_text_controller(): ...
