import os
from typing import AsyncGenerator

from openai import AsyncAzureOpenAI
from fastapi.websockets import WebSocket


class AzureOpenAIChatClient:
    def __init__(self):
        self.aclient = AsyncAzureOpenAI(
            api_key=os.environ["OPENAI_API_KEY"],
            api_version=os.environ["OPENAI_API_VERSION"],
            azure_endpoint=os.environ["OPENAI_API_ENDPOINT"],
            azure_deployment=os.environ["OPENAI_API_DEPLOYMENT"],
        )

    async def chat_stream(
        self, prompt: str, mode: str = "sse", model: str = "gpt-3.5-turbo"
    ) -> AsyncGenerator[str, None]:
        stream = await self.aclient.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=model,
            stream=True,
        )

        async for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield (
                    f"data: {chunk.choices[0].delta.content}\n\n"
                    if mode == "sse"
                    else chunk.choices[0].delta.content
                )
        if mode == "sse":
            yield f"data: [DONE]\n\n"


class WSConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket) -> None:
        await websocket.close()
        self.active_connections.remove(websocket)

    @staticmethod
    async def receive(websocket: WebSocket) -> str:
        return await websocket.receive_text()

    @staticmethod
    async def send(
        message: str | bytes | list | dict, websocket: WebSocket
    ) -> None:
        if isinstance(message, str):
            await websocket.send_text(message)
        elif isinstance(message, bytes):
            await websocket.send_bytes(message)
        else:
            await websocket.send_json(message)


ws_manager = WSConnectionManager()

azure_chat_client = AzureOpenAIChatClient()
