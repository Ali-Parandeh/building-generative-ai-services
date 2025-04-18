# authorization_api.py (Authorization Service)

from typing import Annotated, Literal

from fastapi import Depends, FastAPI
from pydantic import BaseModel

...  # import services and entities here

CurrentUserDep = Annotated[User, Depends(AuthService.get_current_user)]
ActionRep = Annotated[Literal["READ", "CREATE", "UPDATE", "DELETE"], str]
ResourceDep = Annotated[Resource, Depends(ResourceService.get_resource)]


class AuthorizationResponse(BaseModel):
    allowed: bool


app = FastAPI()

app.get("/authorize")


def authorization_controller(
    user: CurrentUserDep, resource: ResourceDep, action: ActionRep
) -> AuthorizationResponse:
    if user.role == "ADMIN":
        return AuthorizationResponse(allowed=True)
    if action in user.permissions.get(resource.id, []):
        return AuthorizationResponse(allowed=True)
    ...  # Other permission checks
    return AuthorizationResponse(allowed=False)


# genai_api.py (GenAI Service)

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel


class AuthorizationData(BaseModel):
    user_id: int
    resource_id: int
    action: str


authorization_client = ...  # Create authorization client


async def enforce(data: AuthorizationData) -> bool:
    response = await authorization_client.decide(data)
    if response.allowed:
        return True
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Access Denied"
    )


router = APIRouter(
    dependencies=[Depends(enforce)], prefix="/generate", tags=["Resource"]
)


@router.post("/text")
async def generate_text_controller(): ...
