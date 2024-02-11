from fastapi import FastAPI, Query
from models import load_text_model, load_image_model, generate_text, generate_image
import uvicorn

app = FastAPI()


@app.get("/generate/text")
def serve_language_model_controller(prompt=Query(...)):
    pipe = load_text_model()
    output = generate_text(pipe, prompt)
    return output


# @app.get("/generate/image")
# def serve_text_to_image_model_controller(prompt=Query(...)):
#     pipe = load_image_model()
#     output = generate_image(pipe, prompt)
#     return output


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
