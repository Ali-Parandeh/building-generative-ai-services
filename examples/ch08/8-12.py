# routes/resource.py

from fastapi import APIRouter

router = APIRouter(prefix="/generate", tags=["Resource"])


@router.get("/text")
def serve_language_model_controller():
    pass


@router.get("/audio")
def serve_text_to_audio_model_controller():
    pass


...  # Add other controllers to the resource router here

# main.py

from typing import Annotated

import routes
from entities import User
from fastapi import Depends, FastAPI
from services.auth import AuthService

auth_service = AuthService()
AuthenticateUserDep = Annotated[User, Depends(auth_service.get_current_user)]


...

app = FastAPI(lifespan=lifespan)

app.include_router(routes.auth.router, prefix="/auth", tags=["Auth"])
app.include_router(
    routes.resource.router,
    dependencies=[AuthenticateUserDep],
    prefix="/generate",
    tags=["Generate"],
)
...  # Add other routes to the app here
