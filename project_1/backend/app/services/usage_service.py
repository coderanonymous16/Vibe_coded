from __future__ import annotations

from dataclasses import dataclass


@dataclass
class UsageRecord:
    user_id: str
    request_id: str
    model: str
    input_tokens: int
    output_tokens: int
    estimated_cost: float
    latency_ms: float


class UsageTracker:
    def __init__(self):
        self.records: list[UsageRecord] = []

    def record(self, user_id: str, request_id: str, model: str, input_tokens: int, output_tokens: int, estimated_cost: float, latency_ms: float) -> UsageRecord:
        record = UsageRecord(user_id, request_id, model, input_tokens, output_tokens, estimated_cost, latency_ms)
        self.records.append(record)
        return record

    def summarize(self) -> dict:
        return {
            "total_requests": len(self.records),
            "total_cost": sum(record.estimated_cost for record in self.records),
            "average_latency_ms": sum(record.latency_ms for record in self.records) / max(len(self.records), 1),
        }
