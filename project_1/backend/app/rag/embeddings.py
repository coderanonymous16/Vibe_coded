from __future__ import annotations

import hashlib
import math

import numpy as np


class SimpleEmbeddingProvider:
    def __init__(self, embedding_size: int = 32):
        self.embedding_size = embedding_size

    def embed_text(self, text: str) -> np.ndarray:
        vector = np.zeros(self.embedding_size, dtype=float)
        for index, token in enumerate(sorted(set(text.lower().split()))):
            if index >= self.embedding_size:
                break
            digest = int(hashlib.sha256(token.encode("utf-8")).hexdigest(), 16)
            vector[index] = (digest % 1000) / 1000.0
        if np.sum(vector) == 0:
            vector[0] = 1.0
        return vector

    def embed_batch(self, texts: list[str]) -> list[np.ndarray]:
        return [self.embed_text(text) for text in texts]


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    denom = float(np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)
