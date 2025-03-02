# main.py

from fastapi import FastAPI
from openai import OpenAI

app = FastAPI()
openai_client = OpenAI()
system_prompt = "You are a helpful assistant."


@app.get("/generate/openai/text")
def serve_openai_language_model_controller(prompt: str) -> str | None:
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"{system_prompt}"},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content
