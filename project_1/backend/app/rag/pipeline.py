from __future__ import annotations

from app.rag.generator import Generator
from app.rag.retriever import Retriever


class RagPipeline:
    def __init__(self, chunks: list[dict] | None = None):
        self.chunks = chunks or []
        self.retriever = Retriever(self.chunks)
        self.generator = Generator()

    def set_chunks(self, chunks: list[dict]) -> None:
        self.chunks = chunks
        self.retriever.set_chunks(chunks)

    def answer(self, question: str, language: str = "english", filters: dict | None = None) -> dict:
        hits = self.retriever.retrieve(question, top_k=5, filters=filters)
        result = self.generator.generate(question, hits, language=language)
        result["retrieved_chunks"] = hits
        return result
