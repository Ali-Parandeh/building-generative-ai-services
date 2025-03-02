# Add required imports here
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from gptcache import Config, cache
from gptcache.embedding import Onnx
from gptcache.processor.post import random_one
from gptcache.processor.pre import last_content
from gptcache.similarity_evaluation import OnnxModelEvaluation


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    cache.init(
        post_func=random_one,
        pre_embedding_func=last_content,
        embedding_func=Onnx().to_embeddings,
        similarity_evaluation=OnnxModelEvaluation(),
        config=Config(similarity_threshold=0.75),
    )
    cache.set_openai_key()
    yield


app = FastAPI(lifespan=lifespan)
