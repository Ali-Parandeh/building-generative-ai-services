import os

from loguru import logger
from qdrant_client import AsyncQdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import ScoredPoint
from transform import clean, embed, load


class VectorRepository:
    def __init__(self, host: str, port: int = 6333) -> None:
        self.db_client = AsyncQdrantClient(host=host, port=port)

    async def create_collection(self, collection_name: str, size: int) -> bool:
        vectors_config = models.VectorParams(
            size=size, distance=models.Distance.COSINE
        )
        response = await self.db_client.get_collections()

        collection_exists = any(
            collection.name == collection_name
            for collection in response.collections
        )
        if collection_exists:
            logger.debug(
                f"Collection {collection_name} already exists - recreating it"
            )
            await self.db_client.delete_collection(collection_name)
            return await self.db_client.create_collection(
                collection_name,
                vectors_config=vectors_config,
            )

        logger.debug(f"Creating collection {collection_name}")
        return await self.db_client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=size, distance=models.Distance.COSINE
            ),
        )

    async def delete_collection(self, name: str) -> bool:
        return await self.db_client.delete_collection(name)

    async def create(
        self,
        collection_name: str,
        embedding_vector: list[float],
        original_text: str,
        source: str,
    ) -> None:
        response = await self.db_client.count(collection_name=collection_name)
        await self.db_client.upsert(
            collection_name=collection_name,
            points=[
                models.PointStruct(
                    id=response.count,
                    vector=embedding_vector,
                    payload={
                        "source": source,
                        "original_text": original_text,
                    },
                )
            ],
        )

    async def search(
        self,
        collection_name: str,
        query_vector: list[float],
        retrieval_limit: int,
        score_threshold: float,
    ) -> list[ScoredPoint]:
        vectors = await self.db_client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=retrieval_limit,
            score_threshold=score_threshold,
        )
        return vectors


vector_repo = VectorRepository(host="localhost", port=6333)


async def store_file_content_in_db(
    filepath: str,
    chunk_size: int = 512,
    collection_name: str = "knowledgebase",
    collection_size: int = 768,
) -> None:
    await vector_repo.create_collection(collection_name, collection_size)
    logger.debug(f"Inserting {filepath} content into database")
    async for chunk in load(filepath, chunk_size):
        logger.debug(f"Inserting '{chunk[0:20]}...' into database")

        embedding_vector = embed(clean(chunk))
        filename = os.path.basename(filepath)
        await vector_repo.create(
            collection_name, embedding_vector, chunk, filename
        )
