from fastapi import FastAPI
from models import load_image_model

models = {}

app = FastAPI()


@app.on_event("startup")
def startup_event():
    models["text2image"] = load_image_model()


@app.on_event("shutdown")
def shutdown_event():
    with open("log.txt", mode="a") as logfile:
        logfile.write("Application shutdown")
