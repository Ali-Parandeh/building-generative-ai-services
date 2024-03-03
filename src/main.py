import time
from contextlib import asynccontextmanager

import uvicorn
from PIL import Image
from fastapi import FastAPI, Query, Response, status, BackgroundTasks, Request
from fastapi.responses import RedirectResponse

from models import generate_image, generate_text, load_image_model, load_text_model
from utils import img_to_bytes

models = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    models["text"] = load_text_model()
    yield
    models.clear()


app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def monitor_service(req: Request, call_next):
    start_time = time.time()
    response = await call_next(req)
    duration = round(time.time() - start_time, 4)
    prompt = req.query_params.get("prompt", "")
    response.headers["X-Response-Time"] = str(duration)
    with open("usage.log", "a") as file:
        file.write(
            f"Endpoint triggered: {req.url}"
            f"\nPrompt: {prompt}"
            f"\nProcessing time: {duration} seconds"
            f"\nStatus Code: {response.status_code}\n\n"
        )
    return response


def process_image_generation(prompt: str) -> None:
    output = generate_image(models["image"], prompt)
    output.save("output.png")


@app.get("/", include_in_schema=False)
def docs_redirect_controller():
    return RedirectResponse(url="/docs", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/generate/text")
def serve_language_model_controller(prompt=Query(...)):
    output = generate_text(models["text"], prompt)
    return output


@app.get("/generate/test")
def serve_language_model_controller(prompt=Query(...)):
    output = "So so good"
    return output


@app.get(
    "/generate/image",
    responses={status.HTTP_200_OK: {"content": {"image/png": {}}}},
    response_class=Response,
)
def serve_text_to_image_model_controller(prompt=Query(...)):
    pipe = load_image_model()
    output = generate_image(pipe, prompt)
    return Response(content=img_to_bytes(output), media_type="image/png")


@app.post("/generate/image/background")
async def serve_image_model_background_controller(background_tasks: BackgroundTasks, prompt: str):
    background_tasks.add_task(process_image_generation, prompt)
    return {"message": "Task is being processed in the background"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
