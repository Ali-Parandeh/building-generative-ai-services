from fastapi import APIRouter
from fastapi_cache.decorator import cache

router = APIRouter(prefix="/generate", tags=["Resource"])


@cache()
async def classify_document(title: str) -> str:
    pass


@router.post("/generate/text")
@cache(expire=60)
async def serve_text_to_text_controller():
    pass
