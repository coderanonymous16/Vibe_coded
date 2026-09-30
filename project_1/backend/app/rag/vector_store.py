from __future__ import annotations

from collections.abc import Iterable

import numpy as np

from app.rag.embeddings import cosine_similarity


class VectorStore:
    def __init__(self):
        self.items: list[dict] = []

    def add(self, chunk: dict, embedding: np.ndarray) -> None:
        self.items.append({"chunk": chunk, "embedding": embedding})

    def add_many(self, chunks: Iterable[dict], embeddings: Iterable[np.ndarray]) -> None:
        for chunk, embedding in zip(chunks, embeddings):
            self.add(chunk, embedding)

    def search(self, query_embedding: np.ndarray, top_k: int = 5, filters: dict | None = None) -> list[dict]:
        matches: list[dict] = []
        for item in self.items:
            metadata = item["chunk"].get("metadata", {})
            if filters:
                for key, value in filters.items():
                    if metadata.get(key) != value:
                        break
                else:
                    matches.append(item)
            else:
                matches.append(item)

        scored = []
        for item in matches:
            score = cosine_similarity(query_embedding, item["embedding"])
            scored.append({"score": score, "chunk": item["chunk"]})
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_k]
