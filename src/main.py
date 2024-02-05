from fastapi import FastAPI, Query
from models import load_model, predict
import uvicorn

app = FastAPI()


@app.get("/generate")
def serve_language_model_controller(prompt: str = Query(...)):
    pipe = load_model()
    output = predict(pipe, prompt)
    return output


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
