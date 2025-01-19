from fastapi import FastAPI, HTTPException, Request, status
from pydantic import BaseModel

app = FastAPI()


class AuthorizationData(BaseModel):
    actor: str
    resource: str
    action: str


def authorize(data: AuthorizationData) -> bool:
    # Placeholder for actual authorization logic
    # This should call the Authorization Logic service and return True if allowed, False otherwise
    if data.actor == "admin" and data.action == "read":
        return True
    return False


@app.post("/enforce")
async def enforce(request: Request):
    data = await request.json()
    auth_data = AuthorizationData(**data)

    is_allowed = authorize(auth_data)
    if is_allowed:
        return {"status": "allowed", "resource": "Here is your resource"}
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")


# To run the app, use the command: uvicorn main:app --reload
