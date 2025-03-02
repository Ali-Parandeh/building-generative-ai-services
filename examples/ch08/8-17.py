# main.py

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

...

app = FastAPI(lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key="your_secret_key")
