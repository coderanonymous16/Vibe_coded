from __future__ import annotations

from fastapi import APIRouter

from app.services.usage_service import UsageTracker

router = APIRouter(tags=["usage"])
tracker = UsageTracker()


@router.get("/usage/summary")
async def usage_summary() -> dict:
    return tracker.summarize()


@router.post("/usage/record")
async def record_usage(
    user_id: str,
    request_id: str,
    model: str,
    input_tokens: int,
    output_tokens: int,
    estimated_cost: float,
    latency_ms: float,
) -> dict:
    record = tracker.record(
        user_id=user_id,
        request_id=request_id,
        model=model,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        estimated_cost=estimated_cost,
        latency_ms=latency_ms,
    )
    return {
        "status": "recorded",
        "record": {
            "user_id": record.user_id,
            "request_id": record.request_id,
            "model": record.model,
            "estimated_cost": record.estimated_cost,
        },
    }
