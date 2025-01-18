# database.py

from entities import Base
from sqlalchemy.ext.asyncio import create_async_engine

database_url = "postgresql+psycopg://fastapi:mysecretpassword@localhost:5432/backend_db"
engine = create_async_engine(database_url, echo=True)


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


# main.py

from contextlib import asynccontextmanager

from database import engine, init_db
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    # other startup operations within the lifespan
    ...
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
