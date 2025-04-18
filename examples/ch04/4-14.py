# main.py

from fastapi import Body, FastAPI, HTTPException, Request, status
from models import generate_text
from schemas import TextModelRequest, TextModelResponse

# load lifespan
...

app = FastAPI(lifespan=lifespan)


@app.post("/generate/text")
def serve_text_to_text_controller(
    request: Request, body: TextModelRequest = Body(...)
) -> TextModelResponse:
    if body.model not in ["tinyLlama", "gemma2b"]:
        raise HTTPException(
            detail=f"Model {body.model} is not supported",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    output = generate_text(models["text"], body.prompt, body.temperature)
    return TextModelResponse(content=output, ip=request.client.host)
