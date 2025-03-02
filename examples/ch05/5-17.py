# main.py

from fastapi import FastAPI, Request
from schemas import TextModelRequest, TextModelResponse
from models import generate_text

# Remove the asynccontextmanager to remove tinyLlama from FastAPI <1>
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     models["text"] = load_text_model()
#     yield
#     models.clear()

# Remove the `lifespan` argument from `FastAPI()`
app = FastAPI()


@app.post("/generate/text")
async def serve_text_to_text_controller(
    request: Request, body: TextModelRequest
) -> TextModelResponse:
    ...  # controller logic
    output = await generate_text(body.prompt, body.temperature)
    return TextModelResponse(content=output, ip=request.client.host)
