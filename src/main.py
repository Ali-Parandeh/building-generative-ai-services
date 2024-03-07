import time
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Callable
from uuid import uuid4

import uvicorn
from fastapi import (BackgroundTasks, Body, FastAPI, HTTPException, Query,
                     Request, Response, status)
from fastapi.responses import RedirectResponse

from models import (generate_image, generate_text, load_image_model,
                    load_text_model)
from schemas import ImageModelRequest, TextModelRequest, TextModelResponse
from utils import img_to_bytes

models = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    models["text"] = load_text_model()
    yield
    models.clear()


app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def monitor_service(req: Request, call_next: Callable) -> Response:
    start_time = time.time()
    response: Response = await call_next(req)
    response_time = round(time.time() - start_time, 4)
    request_id = uuid4().hex
    response.headers["X-Response-Time"] = str(response_time)
    response.headers["X-API-Request-ID"] = request_id
    with open("usage.log", "a") as file:
        file.write(
            f"Request ID: {request_id}"
            f"\nDatetime: {datetime.utcnow().isoformat()}"
            f"\nEndpoint triggered: {req.url}"
            f"\nClient IP Address: {req.client.host}"
            f"\nResponse time: {response_time} seconds"
            f"\nStatus Code: {response.status_code}"
            f"\nSuccessful: {response.status_code < 400}\n\n"
        )
    return response


def process_image_generation(prompt: str) -> None:
    output = generate_image(models["image"], prompt)
    output.save("output.png")


@app.get("/", include_in_schema=False)
def docs_redirect_controller():
    return RedirectResponse(url="/docs", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/generate/text", response_model_exclude_defaults=True)
def serve_text_to_text_controller(request: Request, body: TextModelRequest = Body(...)) -> TextModelResponse:
    if body.model not in ["tinyllama", "gemma2b"]:
        raise HTTPException(detail=f"Model {body.model} is not supported", status_code=status.HTTP_400_BAD_REQUEST)
    # output = generate_text(models["text"], body.prompt, body.temperature)
    return TextModelResponse(content="dsadas dasdsad dasdas", ip=request.client.host)


@app.get(
    "/generate/image",
    responses={status.HTTP_200_OK: {"content": {"image/png": {}}}},
    response_class=Response,
)
def serve_text_to_image_model_controller(body: ImageModelRequest = Body(...)):
    pipe = load_image_model()
    output = generate_image(pipe, body.prompt)
    return Response(content=img_to_bytes(output), media_type="image/png")


@app.post("/generate/image/background")
async def serve_image_model_background_controller(background_tasks: BackgroundTasks, prompt: str):
    background_tasks.add_task(process_image_generation, prompt)
    return {"message": "Task is being processed in the background"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
