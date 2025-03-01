import secrets
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()
security = HTTPBasic()
username_bytes = b"ali"
password_bytes = b"secretpassword"


def authenticate_user(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
) -> str | None:
    is_correct_username = secrets.compare_digest(
        credentials.username.encode("UTF-8"), username_bytes
    )
    is_correct_password = secrets.compare_digest(
        credentials.password.encode("UTF-8"), password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


AuthenticatedUserDep = Annotated[str, Depends(authenticate_user)]


@app.get("/users/me")
def get_current_user_controller(username: AuthenticatedUserDep):
    return {"message": f"Current user is {username}"}
