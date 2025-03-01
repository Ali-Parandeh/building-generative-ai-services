import uuid

from qdrant_client import AsyncQdrantClient, models
from qdrant_client.http.models import Distance, PointStruct, ScoredPoint


class CacheClient:
    def __init__(self):
        self.db = AsyncQdrantClient(":memory:")
        self.cache_collection_name = "cache"

    async def init_db(self) -> None:
        await self.db.create_collection(
            collection_name=self.cache_collection_name,
            vectors_config=models.VectorParams(
                size=384, distance=Distance.EUCLID
            ),
        )

    async def insert(
        self, query_vector: list[float], documents: list[str]
    ) -> None:
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=query_vector,
            payload={"documents": documents},
        )
        await self.db.upload_points(
            collection_name=self.cache_collection_name, points=[point]
        )

    async def search(self, query_vector: list[float]) -> list[ScoredPoint]:
        return await self.db.search(
            collection_name=self.cache_collection_name,
            query_vector=query_vector,
            limit=1,
        )
