# dependencies/auth.py

from entities import User
from fastapi import Depends, HTTPException, status
from services.auth import AuthService


async def is_admin(user: User = Depends(AuthService.get_current_user)) -> User:
    if user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to perform this action",
        )
    return user


# routes/resource.py

from dependencies.auth import is_admin
from fastapi import APIRouter, Depends
from services.auth import AuthService

router = APIRouter(
    dependencies=[Depends(AuthService.get_current_user)],
    prefix="/generate",
    tags=["Resource"],
)


@router.post("/image", dependencies=[Depends(is_admin)])
async def generate_image_controller(): ...


@router.post("/text")
async def generate_text_controller(): ...
