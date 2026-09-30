from __future__ import annotations

import json
from pathlib import Path

from app.rag.pipeline import RagPipeline


class ChatService:
    def __init__(self, chunks: list[dict] | None = None):
        self.pipeline = RagPipeline(chunks or self._load_default_chunks())

    @staticmethod
    def _load_default_chunks() -> list[dict]:
        project_root = Path(__file__).resolve().parents[3]
        sample_path = project_root / "data" / "sample_chunks.json"
        if sample_path.exists():
            payload = json.loads(sample_path.read_text(encoding="utf-8"))
            if isinstance(payload, list):
                return payload
        return []

    def answer_question(self, question: str, language: str = "english", filters: dict | None = None) -> dict:
        return self.pipeline.answer(question, language=language, filters=filters)
