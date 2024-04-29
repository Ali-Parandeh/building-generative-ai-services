import time
from contextlib import asynccontextmanager
from datetime import datetime
from io import BytesIO
from typing import Callable
from uuid import uuid4

import uvicorn
from fastapi import (BackgroundTasks, Body, Depends, FastAPI, HTTPException,
                     Query, Request, Response, UploadFile, status)
from fastapi.responses import RedirectResponse, StreamingResponse
from PIL import Image

from dependencies import get_urls_content
from models import (generate_3d_geometry, generate_audio, generate_image,
                    generate_text, generate_video, load_3d_model,
                    load_audio_model, load_image_model, load_text_model,
                    load_video_model)
from schemas import (ImageModelRequest, TextModelRequest, TextModelResponse,
                     VoicePresets)
from utils import (audio_array_to_buffer, export_to_video_buffer, img_to_bytes,
                   mesh_to_obj_buffer)

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
def serve_text_to_text_controller(
    request: Request,
    body: TextModelRequest = Body(...),
    urls_content: str = Depends(get_urls_content),
) -> TextModelResponse:
    if body.model not in ["tinyllama", "gemma2b"]:
        raise HTTPException(
            detail=f"Model {body.model} is not supported",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    prompt = body.prompt + " " + urls_content
    output = generate_text(models["text"], prompt, body.temperature)
    return TextModelResponse(content=output, ip=request.client.host)


@app.post(
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


@app.post(
    "/generate/audio",
    responses={status.HTTP_200_OK: {"content": {"audio/wav": {}}}},
    response_class=StreamingResponse,
)
def serve_text_to_audio_model_controller(
    prompt=Body(...),
    preset: VoicePresets = Body(default="v2/en_speaker_1"),
):
    processor, model = load_audio_model()
    output, sample_rate = generate_audio(processor, model, prompt, preset)
    return StreamingResponse(audio_array_to_buffer(output, sample_rate), media_type="audio/wav")


@app.post(
    "/generate/video",
    responses={status.HTTP_200_OK: {"content": {"video/mpeg": {}}}},
    response_class=StreamingResponse,
)
async def serve_image_to_video_model_controller(
    image: UploadFile, num_frames: int = Body(default=25)
):
    model = load_video_model()
    image = Image.frombytes(
        data=BytesIO(await image.read()), mode="RGB", size=(image.size, image.size)
    )
    frames = generate_video(model, image, num_frames)
    return StreamingResponse(export_to_video_buffer(frames), media_type="video/mp4")


@app.get(
    "/generate/3d",
    responses={status.HTTP_200_OK: {"content": {"model/obj": {}}}},
    response_class=StreamingResponse,
)
def serve_text_to_3d_model_controller(
    prompt: str = Query(...), num_inference_steps: int = Query(default=25)
):
    model = load_3d_model()
    mesh = generate_3d_geometry(model, prompt, num_inference_steps)
    response = StreamingResponse(mesh_to_obj_buffer(mesh), media_type="model/obj")
    response.headers["Content-Disposition"] = f"attachment; filename={prompt}.obj"
    return response


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
