from fastapi import APIRouter, HTTPException

from app.core.rate_limit import RateLimiter, check_rate_limit
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter(tags=["chat"])
service = ChatService()
rate_limiter = RateLimiter(limit=20, window_seconds=60)


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    if not check_rate_limit(rate_limiter, "global-chat"):
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Please wait before sending another question.")

    result = service.answer_question(request.question, language=request.language, filters=request.filters)
    return ChatResponse(
        answer=result["answer"],
        citations=result.get("citations", []),
        retrieved_chunks=result.get("retrieved_chunks", []),
    )
