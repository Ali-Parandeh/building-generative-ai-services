from qdrant_client import AsyncQdrantClient, models
from qdrant_client.http.models import Distance, ScoredPoint

documents = [...]


class DocumentStoreClient:
    def __init__(self, host="localhost", port=6333):
        self.db_client = AsyncQdrantClient(host=host, port=port)
        self.collection_name = "docs"

    async def init_db(self) -> None:
        await self.db_client.create_collection(
            collection_name=self.collection_name,
            vectors_config=models.VectorParams(
                size=384, distance=Distance.EUCLID
            ),
        )
        await self.db_client.add(
            documents=documents, collection_name=self.collection_name
        )

    async def search(self, query_vector: list[float]) -> list[ScoredPoint]:
        results = await self.db_client.search(
            query_vector=query_vector,
            limit=3,
            collection_name=self.collection_name,
        )
        return results
