from __future__ import annotations

from openai import OpenAI

from app.core.config import settings


class LLMService:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

    def generate(self, question: str, context: str, language: str = "english") -> str:
        if not self.client:
            return ""

        try:
            system_prompt = (
                "You are ExamRAG, an academic assistant. Use only the provided academic context to answer. "
                "If the context is insufficient, say so clearly. Keep the answer concise, accurate, and source-grounded."
            )
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Language: {language}\nQuestion: {question}\n\nAcademic context:\n{context[:5000]}"},
                ],
                temperature=0.2,
                max_tokens=500,
            )
            return response.choices[0].message.content.strip() if response.choices else ""
        except Exception:
            return ""
