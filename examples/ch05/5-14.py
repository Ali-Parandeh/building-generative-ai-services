# dependencies.py

from fastapi import Body
from rag import vector_service
from rag.transform import embed
from schemas import TextModelRequest, TextModelResponse


async def get_rag_content(body: TextModelRequest = Body(...)) -> str:
    rag_content = await vector_service.search("knowledgebase", embed(body.prompt), 3, 0.7)
    rag_content_str = "\n".join([c.payload["original_text"] for c in rag_content])

    return rag_content_str


# main.py

from fastapi import FastAPI, Body, Depends, Request
from dependencies import TextModelRequest
from dependencies import get_rag_content, get_urls_content
from models import generate_text

app = FastAPI()


@app.post("/generate/text", response_model_exclude_defaults=True)
async def serve_text_to_text_controller(
    request: Request,
    body: TextModelRequest = Body(...),
    urls_content: str = Depends(get_urls_content),
    rag_content: str = Depends(get_rag_content),
) -> TextModelResponse:
    ...  # Raise HTTPException for invalid models
    prompt = body.prompt + " " + urls_content + rag_content
    output = generate_text(models["text"], prompt, body.temperature)
    return TextModelResponse(content=output, ip=request.client.host)
