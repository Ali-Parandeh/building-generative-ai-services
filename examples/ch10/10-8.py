import time

from loguru import logger
from transformers import AutoModel

...


class SemanticCacheService:
    def __init__(self, threshold: float = 0.35):
        self.embedder = AutoModel.from_pretrained(
            "jinaai/jina-embeddings-v2-base-en", trust_remote_code=True
        )
        self.euclidean_threshold = threshold
        self.cache_client = CacheClient()
        self.doc_db_client = DocumentStoreClient()

    def get_embedding(self, question) -> list[float]:
        return list(self.embedder.embed(question))[0]

    async def initialize_databases(self):
        await self.cache_client.initialize_databases()
        await self.doc_db_client.initialize_databases()

    async def ask(self, query: str) -> str:
        start_time = time.time()
        vector = self.get_embedding(query)
        if search_results := await self.cache_client.search(vector):
            for s in search_results:
                if s.score <= self.euclidean_threshold:
                    logger.debug(f"Found cache with score {s.score:.3f}")
                    elapsed_time = time.time() - start_time
                    logger.debug(f"Time taken: {elapsed_time:.3f} seconds")
                    return s.payload["content"]

        if db_results := await self.doc_db_client.search(vector):
            documents = [r.payload["content"] for r in db_results]
            await self.cache_client.insert(vector, documents)
            logger.debug("Query context inserted to Cache.")
            elapsed_time = time.time() - start_time
            logger.debug(f"Time taken: {elapsed_time:.3f} seconds")

        logger.debug("No answer found in Cache or Database.")
        elapsed_time = time.time() - start_time
        logger.debug(f"Time taken: {elapsed_time:.3f} seconds")
        return "No answer available."
