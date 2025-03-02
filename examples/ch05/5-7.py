# dependencies.py

from fastapi import Body
from loguru import logger

from schemas import TextModelRequest
from scraper import extract_urls, fetch_all


async def get_urls_content(body: TextModelRequest = Body(...)) -> str:
    urls = extract_urls(body.prompt)
    if urls:
        try:
            urls_content = await fetch_all(urls)
            return urls_content
        except Exception as e:
            logger.warning(f"Failed to fetch one or several URls - Error: {e}")
    return ""


# main.py

from fastapi import FastAPI, Body, Depends, Request
from dependencies import construct_prompt
from schemas import TextModelResponse

app = FastAPI()


@app.post("/generate/text", response_model_exclude_defaults=True)
async def serve_text_to_text_controller(
    request: Request,
    body: TextModelRequest = Body(...),
    urls_content: str = Depends(get_urls_content),
) -> TextModelResponse:
    ...  # rest of controller logic
    prompt = body.prompt + " " + urls_content
    output = generate_text(models["text"], prompt, body.temperature)
    return TextModelResponse(content=output, ip=request.client.host)
