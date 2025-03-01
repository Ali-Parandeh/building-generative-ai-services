# routes/auth.py

from dependencies.auth import ExchangeCodeTokenDep
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse

router = APIRouter()

...


def check_csrf_state(request: Request, state: str) -> None:
    if state != request.session.get("x-csrf-token"):
        raise HTTPException(detail="Bad request", status_code=401)


@router.get("/oauth/github/callback", dependencies=[Depends(check_csrf_state)])
async def oauth_github_callback_controller(
    access_token: ExchangeCodeTokenDep,
) -> RedirectResponse:
    response = RedirectResponse(url=f"http://localhost:8501")
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response
