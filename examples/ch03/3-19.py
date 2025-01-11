# main.py

import httpx
from fastapi import FastAPI, Response, status
from utils import img_to_bytes

app = FastAPI()


@app.get(
    "/generate/image",
    responses={status.HTTP_200_OK: {"content": {"image/png": {}}}},
    response_class=Response,
)
async def generate_image_controller(prompt: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:5000/generate", json={"prompt": prompt}
        )
    return Response(
        content=img_to_bytes(response.content), media_type="image/png"
    )
