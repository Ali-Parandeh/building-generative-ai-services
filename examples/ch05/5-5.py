import os
from fastapi import FastAPI
from openai import AsyncOpenAI, OpenAI

app = FastAPI()

sync_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
async_client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


@app.get("/block")
async def block_server_controller():
    completion = sync_client.chat.completions.create(...)
    return completion.choices[0].message.content


@app.get("/slow")
def slow_text_generator():
    completion = sync_client.chat.completions.create(...)
    return completion.choices[0].message.content


@app.get("/fast")
async def fast_text_generator():
    completion = await async_client.chat.completions.create(...)
    return completion.choices[0].message.content
