from __future__ import annotations


def build_prompt(question: str, context: str, language: str = "english") -> str:
    return f"""You are an academic study assistant. Answer only using the provided evidence.

Language preference: {language}.

Question:
{question}

Context:
{context}

If the evidence is insufficient, explicitly say that you could not find enough information in the provided sources.
"""
