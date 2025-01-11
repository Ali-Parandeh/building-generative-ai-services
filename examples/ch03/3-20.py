# main.py

from fastapi import FastAPI
import openai

app = FastAPI()
system_prompt = "You are a helpful assistant."


@app.get("/generate/openai/text")
def serve_openai_language_model_controller(prompt: str) -> list[str]:
    messages = [
        {"role": "system", "content": f"{system_prompt}"},
        {"role": "user", "content": prompt},
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )

    generated_texts = [
        choice.message["content"].strip() for choice in response["choices"]
    ]
    return generated_texts
