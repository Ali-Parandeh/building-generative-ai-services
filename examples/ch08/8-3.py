# schemas.py

from datetime import datetime
from typing import Annotated

from pydantic import (UUID4, AfterValidator, BaseModel, ConfigDict, Field,
                      validate_call)


@validate_call
def validate_username(value: str) -> str:
    if not value.isalnum():
        raise ValueError("Username must be alphanumeric")
    return value


@validate_call
def validate_password(value: str) -> str:
    validations = [
        (
            lambda v: any(char.isdigit() for char in v),
            "Password must contain at least one digit",
        ),
        (
            lambda v: any(char.isupper() for char in v),
            "Password must contain at least one uppercase letter",
        ),
        (
            lambda v: any(char.islower() for char in v),
            "Password must contain at least one lowercase letter",
        ),
    ]
    for condition, error_message in validations:
        if not condition(value):
            raise ValueError(error_message)
    return value


ValidUsername = Annotated[
    str, Field(min_length=3, max_length=20), AfterValidator(validate_username)
]
ValidPassword = Annotated[
    str, Field(min_length=8, max_length=64), AfterValidator(validate_password)
]


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: ValidUsername
    is_active: bool = True
    role: str = "USER"


class UserCreate(UserBase):
    password: ValidPassword


class UserInDB(UserBase):
    hashed_password: str


class UserOut(UserBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime
