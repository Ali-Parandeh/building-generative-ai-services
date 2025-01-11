from contextlib import asynccontextmanager
from typing import AsyncIterator, Awaitable, Callable
from io import BytesIO
import csv
import time
from datetime import datetime, timezone
from uuid import uuid4

import httpx
import openai
from PIL import Image
from fastapi import FastAPI, status, File, Request, Response
from fastapi.responses import StreamingResponse
from openai import OpenAI
from models import (
    load_text_model,
    generate_text,
    load_image_model,
    generate_image,
    load_audio_model,
    generate_audio,
    load_video_model,
    generate_video,
    load_3d_model,
    generate_3d_geometry,
)
from schemas import VoicePresets
from utils import (
    audio_array_to_buffer,
    img_to_bytes,
    export_to_video_buffer,
    mesh_to_obj_buffer,
)

openai_client = OpenAI()
system_prompt = "You are a helpful assistant."

models = {}


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    models["text2image"] = load_image_model()

    yield

    ...  # Run cleanup code here

    models.clear()


app = FastAPI(lifespan=lifespan)

csv_header = [
    "Request ID",
    "Datetime",
    "Endpoint Triggered",
    "Client IP Address",
    "Response Time",
    "Status Code",
    "Successful",
]


@app.middleware("http")
async def monitor_service(
    req: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    request_datetime = datetime.now(timezone.utc).isoformat()
    start_time = time.perf_counter()
    request_id = uuid4().hex
    req.headers["X-API-Request-ID"] = request_id
    response: Response = await call_next(req)
    response_time = round(time.perf_counter() - start_time, 4)
    response.headers["X-Response-Time"] = str(response_time)
    response.headers["X-API-Request-ID"] = request_id
    with open("usage.csv", "a", newline="") as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(csv_header)
        writer.writerow(
            [
                request_id,
                request_datetime,
                req.url,
                req.client.host,
                response_time,
                response.status_code,
                response.status_code < 400,
            ]
        )
    return response


@app.get("/")
def root_controller():
    return {"status": "healthy"}


@app.get("/chat")
def chat_controller(prompt: str = "Inspire me"):
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    statement = response.choices[0].message.content.strip()
    return {"statement": statement}


@app.get("/generate/text")
def serve_language_model_controller(prompt: str) -> str:
    pipe = load_text_model()
    output = generate_text(pipe, prompt)
    return output


@app.get(
    "/generate/audio",
    responses={status.HTTP_200_OK: {"content": {"audio/wav": {}}}},
    response_class=StreamingResponse,
)
def serve_text_to_audio_model_controller(
    prompt: str,
    preset: VoicePresets = "v2/en_speaker_1",
):
    processor, model = load_audio_model()
    output, sample_rate = generate_audio(processor, model, prompt, preset)
    return StreamingResponse(
        audio_array_to_buffer(output, sample_rate), media_type="audio/wav"
    )


@app.get(
    "/generate/image",
    responses={status.HTTP_200_OK: {"content": {"image/png": {}}}},
    response_class=Response,
)
def serve_text_to_image_model_controller(prompt: str):
    output = generate_image(models["text2image"], prompt)
    return Response(content=img_to_bytes(output), media_type="image/png")


@app.post(
    "/generate/video",
    responses={status.HTTP_200_OK: {"content": {"video/mp4": {}}}},
    response_class=StreamingResponse,
)
def serve_image_to_video_model_controller(
    image: bytes = File(...), num_frames: int = 25
):
    image = Image.open(BytesIO(image))
    model = load_video_model()
    frames = generate_video(model, image, num_frames)
    return StreamingResponse(
        export_to_video_buffer(frames), media_type="video/mp4"
    )


@app.get(
    "/generate/3d",
    responses={status.HTTP_200_OK: {"content": {"model/obj": {}}}},
    response_class=StreamingResponse,
)
def serve_text_to_3d_model_controller(
    prompt: str, num_inference_steps: int = 25
):
    model = load_3d_model()
    mesh = generate_3d_geometry(model, prompt, num_inference_steps)
    response = StreamingResponse(
        mesh_to_obj_buffer(mesh), media_type="model/obj"
    )
    response.headers["Content-Disposition"] = (
        f"attachment; filename={prompt}.obj"
    )
    return response


@app.get(
    "/generate/bentoml/image",
    responses={status.HTTP_200_OK: {"content": {"image/png": {}}}},
    response_class=Response,
)
async def serve_bentoml_text_to_image_controller(prompt: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:5000/generate", json={"prompt": prompt}
        )
    return Response(content=response.content, media_type="image/png")


@app.get("/generate/openai/text")
def serve_openai_language_model_controller(prompt: str) -> list[str]:
    messages = [
        {"role": "system", "content": f"{system_prompt}"},
        {"role": "user", "content": prompt},
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )

    generated_texts = [
        choice.message["content"].strip() for choice in response["choices"]
    ]
    return generated_texts
