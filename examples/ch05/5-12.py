# rag/service.py

import os

from loguru import logger
from .repository import VectorRepository
from .transform import clean, embed, load


class VectorService(VectorRepository):
    def __init__(self):
        super().__init__()

    async def store_file_content_in_db(
        self,
        filepath: str,
        chunk_size: int = 512,
        collection_name: str = "knowledgebase",
        collection_size: int = 768,
    ) -> None:
        await self.create_collection(collection_name, collection_size)
        logger.debug(f"Inserting {filepath} content into database")
        async for chunk in load(filepath, chunk_size):
            logger.debug(f"Inserting '{chunk[0:20]}...' into database")

            embedding_vector = embed(clean(chunk))
            filename = os.path.basename(filepath)
            await self.create(collection_name, embedding_vector, chunk, filename)


vector_service = VectorService()
