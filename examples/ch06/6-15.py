# main.py

import asyncio
from fastapi import FastAPI
from fastapi.websockets import WebSocket, WebSocketDisconnect
from loguru import logger
from stream import ws_manager, azure_chat_client

app = FastAPI()


@app.websocket("/generate/text/streams")
async def websocket_endpoint(websocket: WebSocket) -> None:
    logger.info("Connecting to client....")
    await ws_manager.connect(websocket)
    try:
        while True:
            prompt = await ws_manager.receive(websocket)
            async for chunk in azure_chat_client.chat_stream(prompt, "ws"):
                await ws_manager.send(chunk, websocket)
                await asyncio.sleep(0.05)
    except WebSocketDisconnect:
        logger.info("Client disconnected")
    except Exception as e:
        logger.error(f"Error with the WebSocket connection: {e}")
        await ws_manager.send("An internal server error has occurred")
    finally:
        await ws_manager.disconnect(websocket)
