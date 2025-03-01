# routes/auth.py
from typing import Annotated

from entities import User
from fastapi import APIRouter, Depends
from models import TokenOut, UserOut
from services.auth import AuthService

auth_service = AuthService()
RegisterUserDep = Annotated[User, Depends(auth_service.register_user)]
AuthenticateUserCredDep = Annotated[
    str, Depends(auth_service.authenticate_user_with_credentials)
]
AuthenticateUserTokenDep = Annotated[User, Depends(auth_service.register_user)]
PasswordResetDep = Annotated[None, Depends(auth_service.reset_password)]

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
async def register_user_controller(new_user: RegisterUserDep) -> UserOut:
    return new_user


@router.post("/token")
async def login_for_access_token_controller(
    access_token: AuthenticateUserCredDep,
) -> TokenOut:
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout", dependencies=[Depends(auth_service.logout)])
async def logout_access_token_controller() -> dict:
    return {"message": "Logged out"}


@router.post("reset-password")
async def reset_password_controller(credentials: PasswordResetDep) -> dict:
    return {
        "message": "If an account exists, a password reset link will be sent to the provided email"
    }
