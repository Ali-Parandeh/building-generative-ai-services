import uvicorn
from fastapi import FastAPI, Query, Response, status

from models import (generate_image, generate_text, load_image_model,
                    load_text_model)
from utils import img_to_bytes

app = FastAPI()


@app.get("/generate/text")
def serve_language_model_controller(prompt=Query(...)):
    pipe = load_text_model()
    output = generate_text(pipe, prompt)
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


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
