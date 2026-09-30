from __future__ import annotations

from app.rag.context_builder import build_context
from app.services.llm_service import LLMService


class Generator:
    def __init__(self, provider=None):
        self.provider = provider
        self.llm_service = LLMService()

    def generate(self, question: str, chunks: list[dict], language: str = "english") -> dict:
        context = build_context(chunks)
        if not chunks:
            return {
                "answer": "I couldn't find enough information in the provided academic sources to answer that accurately.",
                "citations": [],
                "context": context,
            }

        citations = [
            {
                "document": chunk.get("metadata", {}).get("title", "Unknown document"),
                "page": chunk.get("page"),
                "chunk_id": chunk.get("chunk_id"),
            }
            for chunk in chunks
        ]

        llm_answer = self.llm_service.generate(question, context, language=language)
        if llm_answer:
            return {
                "answer": llm_answer,
                "citations": citations,
                "context": context,
            }

        answer = f"Based on the relevant academic material, here is the answer in {language}:\n\n"
        answer += context[:600]
        return {
            "answer": answer,
            "citations": citations,
            "context": context,
        }
