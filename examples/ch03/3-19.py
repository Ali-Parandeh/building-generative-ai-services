# main.py

import httpx
from fastapi import FastAPI, Response, status

app = FastAPI()


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
