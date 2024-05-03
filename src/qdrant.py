from loguru import logger
from qdrant_client import AsyncQdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import ScoredPoint


class VectorRepository:
    def __init__(self, host: str, port: int) -> None:
        self.client = AsyncQdrantClient(host=host, port=port)

    async def create_collection(self, name: str, size: int = 1536):
        response = await self.client.get_collections()
        collection_exists = any(
            collection.name == name for collection in response.collections
        )

        if collection_exists:
            logger.debug(
                f"Collection {name} already exists - skipping collection creation"
            )
            return

        try:
            await self.client.create_collection(
                collection_name=name,
                vectors_config=models.VectorParams(
                    size=size, distance=models.Distance.COSINE
                ),
            )
        except Exception as e:
            logger.error(f"Failed to create collection '{name}' - Error: {e}")

    async def create(
        self,
        collection_name: str,
        embedding_vector: list[float],
        original_text: str,
        source: str,
    ) -> None:
        response = await self.client.count(collection_name=collection_name)
        try:
            await self.client.upsert(
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
            logger.info(
                f"Point id {response.count} has been successfully "
                f"created in collection '{collection_name}'"
            )
        except Exception as e:
            logger.error(
                f"Failed to upload data to collection '{collection_name}': {e}"
            )

    async def search(
        self,
        collection_name: str,
        query_vector: list[float],
        retrieval_limit: int,
    ) -> list[ScoredPoint]:
        try:
            vectors = await self.client.search(
                collection_name=collection_name,
                query_vector=query_vector,
                limit=retrieval_limit,
            )

            logger.info(f"Successfully retrieved {len(vectors)} search results")
        except Exception as e:
            logger.error(f"Failed to retrieve search results: {e}")
            return []

        return vectors
