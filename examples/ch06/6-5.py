# main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/pages", StaticFiles(directory="pages"), name="pages")
