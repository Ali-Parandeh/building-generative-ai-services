from contextlib import asynccontextmanager

import redis
from fastapi import Depends, FastAPI
from fastapi.websockets import WebSocket
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import WebSocketRateLimiter

...


@asynccontextmanager
async def lifespan(_: FastAPI):
    redis_connection = redis.from_url("redis://localhost:6379", encoding="utf8")
    await FastAPILimiter.init(redis_connection)
    yield
    await FastAPILimiter.close()


app = FastAPI(lifespan=lifespan)


@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket, user_id: int = Depends(get_current_user)
):
    ratelimit = WebSocketRateLimiter(times=1, seconds=5)
    await ws_manager.connect(websocket)
    try:
        while True:
            prompt = await ws_manager.receive(websocket)
            await ratelimit(websocket, context_key=user_id)
            async for chunk in azure_chat_client.chat_stream(prompt, "ws"):
                await ws_manager.send(chunk, websocket)
    except WebSocketRateLimitException:
        await websocket.send_text(f"Rate limit exceeded. Try again later")
    finally:
        await ws_manager.disconnect(websocket)
