from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1)
    language: str = "english"
    filters: dict | None = None


class ChatResponse(BaseModel):
    answer: str
    citations: list[dict]
    retrieved_chunks: list[dict]
