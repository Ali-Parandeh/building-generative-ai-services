# main.py

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from stream import azure_chat_client

app = FastAPI()


@app.get("/generate/text/stream")
async def serve_text_to_text_stream_controller(
    prompt: str,
) -> StreamingResponse:
    return StreamingResponse(
        azure_chat_client.chat_stream(prompt), media_type="text/event-stream"
    )
