# main.py

from contextlib import asynccontextmanager
from typing import AsyncIterator
from fastapi import FastAPI, Response, status

from models import load_image_model, generate_image
from utils import img_to_bytes

models = {}


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    models["text2image"] = load_image_model()

    yield

    ...  # Run cleanup code here

    models.clear()


app = FastAPI(lifespan=lifespan)


@app.get(
    "/generate/image",
    responses={status.HTTP_200_OK: {"content": {"image/png": {}}}},
    response_class=Response,
)
def serve_text_to_image_model_controller(prompt: str):
    output = generate_image(models["text2image"], prompt)
    return Response(content=img_to_bytes(output), media_type="image/png")
