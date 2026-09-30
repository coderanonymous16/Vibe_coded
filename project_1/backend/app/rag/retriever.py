from __future__ import annotations

from app.rag.bm25 import BM25Retriever
from app.rag.embeddings import SimpleEmbeddingProvider
from app.rag.vector_store import VectorStore


class Retriever:
    def __init__(self, chunks: list[dict] | None = None):
        self.chunks = chunks or []
        self.provider = SimpleEmbeddingProvider()
        self.vector_store = VectorStore()
        self.bm25 = BM25Retriever()
        self._reindex()

    def _reindex(self) -> None:
        texts = [chunk.get("text", "") for chunk in self.chunks]
        self.bm25.index_documents(texts)
        self.vector_store = VectorStore()
        for chunk in self.chunks:
            embedding = self.provider.embed_text(chunk.get("text", ""))
            self.vector_store.add(chunk, embedding)

    def set_chunks(self, chunks: list[dict]) -> None:
        self.chunks = chunks
        self._reindex()

    def retrieve(self, query: str, top_k: int = 5, filters: dict | None = None) -> list[dict]:
        query_embedding = self.provider.embed_text(query)
        vector_hits = self.vector_store.search(query_embedding, top_k=top_k, filters=filters)
        bm25_hits = self.bm25.search(query, top_k=top_k, filters=filters)
        results = []
        for hit in vector_hits:
            results.append({**hit["chunk"], "score": hit["score"], "source": "vector"})
        for hit in bm25_hits:
            results.append({"text": hit["text"], "score": hit["score"], "source": "bm25", "metadata": {}})
        deduped = []
        seen = set()
        for item in results:
            key = item.get("chunk_id") or item.get("text")
            if key in seen:
                continue
            seen.add(key)
            deduped.append(item)
        deduped.sort(key=lambda item: item.get("score", 0.0), reverse=True)
        return deduped[:top_k]
